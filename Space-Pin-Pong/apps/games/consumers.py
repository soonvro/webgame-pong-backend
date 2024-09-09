import asyncio
import json

from apps.games.services import PongGameManager
from channels.generic.websocket import AsyncWebsocketConsumer


class LocalGameConsumer(AsyncWebsocketConsumer):
    _fps: int = 60
    _frame_time: float = 1 / float(_fps)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self._game_manager: PongGameManager = PongGameManager()
        self._game_task: asyncio.Task | None = None
        self._wait_delay: int = 0

    async def connect(self):
        self._game_task = asyncio.create_task(self.game_loop())
        await self.accept()

    async def disconnect(self, close_code):
        await self._game_manager.shutdown()

    async def receive(self, text_data=None, bytes_data=None):
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
        if message_type == "games.inputs":
            player1_direction, player2_direction = text_data_json["inputs"]
            player1_direction = "u" if player1_direction == "r" else "d" if player1_direction == "l" else "n"
            player2_direction = "u" if player2_direction == "r" else "d" if player2_direction == "l" else "n"
            await self._game_manager.move_paddle((player1_direction, player2_direction))

    async def game_loop(self):
        """
        이 메소드는 게임 루프를 나타냅니다.
        게임 루프는 게임이 종료될 때까지 계속해서 반복됩니다.
        """
        self._wait_delay = 3
        while self._wait_delay > 0:
            await self.send(self._serialize_game_state(self._game_manager.state))
            await asyncio.sleep(1)
            self._wait_delay -= 1

        self._game_manager.start()
        frame_count: int = 0
        is_turn_over: bool = False
        while True:
            game_state: dict = self._game_manager.state
            if game_state["state"] == PongGameManager.State.TURN_OVER:
                if not is_turn_over:
                    is_turn_over = True
                    self._wait_delay = 3
                elif self._wait_delay == 0:
                    is_turn_over = False
                    await self._game_manager.resume()

            await self.send(self._serialize_game_state(game_state))

            if game_state["state"] == PongGameManager.State.ENDED:
                break
            await asyncio.sleep(self._frame_time)

            frame_count += 1
            if frame_count == self._fps:
                frame_count = 0
                if self._wait_delay > 0:
                    self._wait_delay -= 1

    def _serialize_game_state(self, game_state: dict) -> str:
        """
        게임 상태를 JSON 형식으로 직렬화합니다.
        """
        wait_state = 2
        if game_state["state"] == PongGameManager.State.TURN_OVER:
            wait_state = 1
        elif game_state["state"] == PongGameManager.State.STARTED:
            wait_state = 0

        data: dict = {
            "type": "games.state",
            "finish": game_state["state"] == PongGameManager.State.ENDED,
            "bar": game_state["paddle_y"],
            "ball": game_state["ball"],
            "score": game_state["score"],
            "wait": [wait_state, self._wait_delay],
        }
        return json.dumps(data)
