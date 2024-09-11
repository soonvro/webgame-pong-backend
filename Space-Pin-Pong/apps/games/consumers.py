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
        self._send_task: asyncio.Task | None = None
        self._wait_delay: int = 0

    async def connect(self):
        await self.accept()

        self._game_task = asyncio.create_task(self._game_manager.game_loop())
        self._send_task = asyncio.create_task(self._send_loop())

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

    async def _send_loop(self):
        """
        이 메소드는 게임의 상태를 클라이언트에 전송하는 루프입니다.
        """
        await self.send(text_data=json.dumps(self._game_manager.get_game_state()))
