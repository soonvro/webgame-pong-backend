import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from apps.games.utils import distance_line_point


class LocalGameConsumer(AsyncWebsocketConsumer):
    game_fps: int = 60
    size_magnification: int = 1000

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.field_width: int = 500 * self.size_magnification
        self.field_height: int = 250 * self.size_magnification
        self.bar_width: int = 10 * self.size_magnification
        self.bar_height: int = 100 * self.size_magnification
        self.ball_radius: int = 7 * self.size_magnification
        self.ball_speed: int = 1000 * self.size_magnification // self.game_fps  # pixel per frame
        self.player_speed: int = 200 * self.size_magnification // self.game_fps  # pixel per frame

        self.ball_pos_x: int = self.field_width // 2
        self.ball_pos_y: int = self.field_height // 2
        self.ball_velocity_x: int = self.ball_speed // 2
        self.ball_velocity_y: int = self.ball_speed // 4

        self.player1_pos_x: int = self.bar_width * 2
        self.player1_pos_y: int = self.field_height // 2

        self.player2_pos_x: int = self.field_width - (self.bar_width * 2)
        self.player2_pos_y: int = self.field_height // 2

        self.player1_score: int = 0
        self.player2_score: int = 0

        self.player1_direction: str = "n"
        self.player2_direction: str = "n"

        self.direction_queue_lock = asyncio.Lock()


    async def connect(self):
        await self.accept()

        await asyncio.create_task(self.loop_game())

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        """
        이 메소드는 서버가 클라이언트로부터 메시지를 받았을 때 호출됩니다.
        메시지는 JSON 형식으로 전달되며, 다음과 같은 형식을 가지고 있습니다:
        {
          "type": "move",
          "directions": [<player1_direction>, <player2_direction>]
        }
        여기서 <player1_direction>과 <player2_direction>은 각각 플레이어 1과 플레이어 2의 이동 방향을 나타냅니다.
        이 값은 'l'(left), 'r'(right), 'n'(none) 중 하나일 수 있습니다.
        """
        text_data_json = json.loads(text_data)
        message_type = text_data_json["type"]
        if message_type == "move":
            player1_direction, player2_direction = text_data_json["directions"]
            await self.update_player_direction(player1_direction, player2_direction)

    async def update_player_direction(self, player1_direction: str, player2_direction: str) -> None:
        async with self.direction_queue_lock:
            self.player1_direction = player1_direction
            self.player2_direction = player2_direction

    async def loop_game(self):
        while True:
            await self.update_game_state()
            await asyncio.sleep(1 / self.game_fps)

    async def update_game_state(self):
        async with self.direction_queue_lock:
            await self.update_player_position()

        await self.update_ball_position()
        print(f"ball: ({self.ball_pos_x}, {self.ball_pos_y}), score: ({self.player1_score}, {self.player2_score})")
        await self.send(
            text_data=json.dumps(
                {
                    "type": "stateUpdate",
                    "ball": [self.ball_pos_x, self.ball_pos_y],
                    "score": [self.player1_score, self.player2_score],
                }
            )
        )

    async def update_player_position(self):
        if self.player1_direction == "l":
            self.player1_pos_y += self.player_speed
        elif self.player1_direction == "r":
            self.player1_pos_y -= self.player_speed
        self.player1_direction = "n"

        if self.player2_direction == "l":
            self.player2_pos_y -= self.player_speed
        elif self.player2_direction == "r":
            self.player2_pos_y += self.player_speed
        self.player2_direction = "n"

    async def update_ball_position(self) -> None:
        self.ball_pos_x += self.ball_velocity_x
        self.ball_pos_y += self.ball_velocity_y

        if self.is_ball_hit_vertical_wall():
            if self.ball_pos_x <= self.ball_radius:
                self.player2_score += 1
            else:
                self.player1_score += 1
        if self.is_ball_hit_bar():
            self.ball_velocity_x *= -1
        if self.is_ball_hit_horizontal_wall():
            self.ball_velocity_y *= -1


    def is_ball_hit_horizontal_wall(self) -> bool:
        return (self.ball_pos_y <= self.ball_radius
                or self.ball_pos_y >= self.field_height - self.ball_radius)

    def is_ball_hit_bar(self) -> bool:
        bar1_top: int = self.player1_pos_y + self.bar_height // 2
        bar1_bottom: int = self.player1_pos_y - self.bar_height // 2
        bar2_top: int = self.player2_pos_y + self.bar_height // 2
        bar2_bottom: int = self.player2_pos_y - self.bar_height // 2

        bar1 = (self.player1_pos_x, bar1_top, self.player1_pos_x, bar1_bottom)
        bar2 = (self.player2_pos_x, bar2_top, self.player2_pos_x, bar2_bottom)

        return (distance_line_point(bar1, (self.ball_pos_x, self.ball_pos_y)) <= self.ball_radius
                or distance_line_point(bar2, (self.ball_pos_x, self.ball_pos_y)) <= self.ball_radius)

    def is_ball_hit_vertical_wall(self) -> bool:
        return (self.ball_pos_x <= self.ball_radius
                or self.ball_pos_x >= self.field_width - self.ball_radius)
