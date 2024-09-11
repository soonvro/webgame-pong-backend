import asyncio
import random
import time
from enum import Enum
from typing import Callable

import numpy as np
from overrides import overrides


class BaseObject:
    def __init__(self, x: int = 0, y: int = 0):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("x and y must be int")
        self._x: int = x
        self._y: int = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def set_position(self, x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("x and y must be int")
        self._x = x
        self._y = y


class MovableObject(BaseObject):
    def __init__(self, x: int = 0, y: int = 0, velocity_x: int = 0, velocity_y: int = 0):
        if not isinstance(velocity_x, int) or not isinstance(velocity_y, int):
            raise TypeError("velocity_x and velocity_y must be int")

        super().__init__(x, y)
        self._velocity_x = velocity_x
        self._velocity_y = velocity_y
        self._x_future: int = 0
        self._y_future: int = 0
        self._cal_future_position()

    @overrides
    def set_position(self, x: int, y: int):
        super().set_position(x, y)
        self._cal_future_position()

    @property
    def velocity(self) -> tuple[int, int]:
        return self._velocity_x, self._velocity_y

    def set_velocity(self, velocity_x: int, velocity_y: int):
        if not isinstance(velocity_x, int) or not isinstance(velocity_y, int):
            raise TypeError("velocity_x and velocity_y must be int")
        self._velocity_x = velocity_x
        self._velocity_y = velocity_y
        self._cal_future_position()

    @property
    def x_future(self) -> int:
        return self._x_future

    @property
    def y_future(self) -> int:
        return self._y_future

    def move(self) -> None:
        super().set_position(self._x_future, self._y_future)
        self._cal_future_position()

    # --------------------------------------------------------------------------
    #  Private methods
    # --------------------------------------------------------------------------
    def _cal_future_position(self) -> None:
        self._x_future = self.x + self._velocity_x
        self._y_future = self.y + self._velocity_y


class GameObject(MovableObject):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        velocity_x: int = 0,
        velocity_y: int = 0,
        x_min_bound: int = 0,
        x_max_bound: int = 100,
        y_min_bound: int = 0,
        y_max_bound: int = 100,
    ):
        if (
            not isinstance(x_min_bound, int)
            or not isinstance(x_max_bound, int)
            or not isinstance(y_min_bound, int)
            or not isinstance(y_max_bound, int)
        ):
            raise TypeError("x_min_bound, x_max_bound, y_min_bound, y_max_bound must be int")

        super().__init__(x, y, velocity_x, velocity_y)
        self._x_min_bound = x_min_bound
        self._x_max_bound = x_max_bound
        self._y_min_bound = y_min_bound
        self._y_max_bound = y_max_bound

    @overrides
    def move(self) -> None:
        if self.is_out_of_bound_future():
            return
        super().move()

    def is_out_of_bound_future(self) -> bool:
        return self.is_out_of_x_bound_future() or self.is_out_of_y_bound_future()

    def is_out_of_x_bound_future(self) -> bool:
        return self.is_less_than_x_min_bound_future() or self.is_greater_than_x_max_bound_future()

    def is_out_of_y_bound_future(self) -> bool:
        return self.is_less_than_y_min_bound_future() or self.is_greater_than_y_max_bound_future()

    def is_less_than_x_min_bound_future(self) -> bool:
        return self._x_future < self._x_min_bound

    def is_greater_than_x_max_bound_future(self) -> bool:
        return self._x_future > self._x_max_bound

    def is_less_than_y_min_bound_future(self) -> bool:
        return self._y_future < self._y_min_bound

    def is_greater_than_y_max_bound_future(self) -> bool:
        return self._y_future > self._y_max_bound


class Paddle(GameObject):
    """
    Paddle object
    input:
        x: int - x position of center
        y: int - y position of center
        width: int - width of paddle
        height: int - height of paddle
        velocity_x: int - velocity of x
        velocity_y: int - velocity of y
        x_min_bound: int - x min bound
        x_max_bound: int - x max bound
        y_min_bound: int - y min bound
        y_max_bound: int - y max bound
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 10,
        height: int = 50,
        velocity_x: int = 0,
        velocity_y: int = 0,
        x_min_bound: int = 0,
        x_max_bound: int = 100,
        y_min_bound: int = 0,
        y_max_bound: int = 100,
    ):
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("width and height must be int")

        super().__init__(
            x,
            y,
            velocity_x,
            velocity_y,
            x_min_bound + width // 2,
            x_max_bound - width // 2,
            y_min_bound + height // 2,
            y_max_bound - height // 2,
        )
        self._width = width
        self._height = height


class Ball(GameObject):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        radius: int = 10,
        velocity_x: int = 0,
        velocity_y: int = 0,
        x_min_bound: int = 0,
        x_max_bound: int = 100,
        y_min_bound: int = 0,
        y_max_bound: int = 100,
    ):
        if not isinstance(radius, int):
            raise TypeError("radius must be int")

        super().__init__(
            x,
            y,
            velocity_x,
            velocity_y,
            x_min_bound + radius,
            x_max_bound - radius,
            y_min_bound + radius,
            y_max_bound - radius,
        )
        self._radius = radius

    @property
    def radius(self) -> int:
        return self._radius


class PongGameEngine:
    X_MIN_IDX = 0
    Y_MIN_IDX = 1
    X_MAX_IDX = 2
    Y_MAX_IDX = 3

    _fps: int = 200
    _frame_time: float = 1 / float(_fps)
    _size_magnification: int = 1000

    class State(Enum):
        NOT_STARTED = "not started"
        STARTED = "started"
        PAUSED = "paused"
        TURN_OVER = "turn over"
        ENDED = "ended"

    def __init__(
        self,
        field_bound: tuple[int, int, int, int] = (-500, -250, 500, 250),  # x_min, y_min, x_max, y_max
        ball_radius: int = 7,
        ball_speed: int = 1000,  # grid per second
        paddle_width: int = 10,
        paddle_height: int = 100,
        distance_paddle_to_wall: int = 0,
        paddle_speed: int = 500,  # grid per second
        max_score: int = 15,
        on_start: Callable[[], None] = (lambda: None),
        on_turn_over: Callable[[], None] = (lambda: None),
        on_end: Callable[[], None] = (lambda: None),
    ):
        if not isinstance(ball_radius, int):
            raise TypeError("ball_radius must be int")
        if not isinstance(ball_speed, int):
            raise TypeError("ball_speed must be int")
        if not isinstance(paddle_width, int) or not isinstance(paddle_height, int):
            raise TypeError("paddle_width and paddle_height must be int")
        if not isinstance(paddle_speed, int):
            raise TypeError("paddle_speed must be int")
        if not isinstance(distance_paddle_to_wall, int):
            raise TypeError("distance_paddle_to_wall must be int")
        if not isinstance(field_bound, tuple) or len(field_bound) != 4:
            raise TypeError("field_bound must be tuple[int, int, int, int]")
        for _i in field_bound:
            if not isinstance(_i, int):
                raise TypeError("field_bound must be tuple[int, int, int, int]")
        if not isinstance(max_score, int):
            raise TypeError("max_score must be int")

        # apply size magnification
        field_bound = tuple([_i * self._size_magnification for _i in field_bound])  # type: ignore
        ball_radius = ball_radius * self._size_magnification
        ball_speed = ball_speed * self._size_magnification
        paddle_width = paddle_width * self._size_magnification
        paddle_height = paddle_height * self._size_magnification
        distance_paddle_to_wall = distance_paddle_to_wall * self._size_magnification
        paddle_speed = paddle_speed * self._size_magnification

        self._initial_ball_pos: tuple[int, int] = (
            (field_bound[self.X_MIN_IDX] + field_bound[self.X_MAX_IDX]) // 2,
            (field_bound[self.Y_MIN_IDX] + field_bound[self.Y_MAX_IDX]) // 2,
        )
        self._ball_speed: int = ball_speed // self._fps
        ball_velocity_x, ball_velocity_y = self._get_ball_initial_velocity()
        self._ball: Ball = Ball(
            x=self._initial_ball_pos[0],
            y=self._initial_ball_pos[1],
            radius=ball_radius,
            velocity_x=ball_velocity_x,
            velocity_y=ball_velocity_y,
            x_min_bound=field_bound[self.X_MIN_IDX],
            x_max_bound=field_bound[self.X_MAX_IDX],
            y_min_bound=field_bound[self.Y_MIN_IDX],
            y_max_bound=field_bound[self.Y_MAX_IDX],
        )

        self._paddle_half_width: int = paddle_width // 2
        self._paddle_half_height: int = paddle_height // 2
        self._left_paddle_initial_pos: tuple[int, int] = (
            field_bound[self.X_MIN_IDX] + distance_paddle_to_wall + self._paddle_half_width,
            (field_bound[self.Y_MIN_IDX] + field_bound[self.Y_MAX_IDX]) // 2,
        )
        self._right_paddle_initial_pos: tuple[int, int] = (
            field_bound[self.X_MAX_IDX] - distance_paddle_to_wall - self._paddle_half_width,
            (field_bound[self.Y_MIN_IDX] + field_bound[self.Y_MAX_IDX]) // 2,
        )
        self._left_paddle: Paddle = Paddle(
            x=self._left_paddle_initial_pos[0],
            y=self._left_paddle_initial_pos[1],
            width=paddle_width,
            height=paddle_height,
            velocity_x=0,
            velocity_y=0,
            x_min_bound=field_bound[self.X_MIN_IDX],
            x_max_bound=field_bound[self.X_MAX_IDX],
            y_min_bound=field_bound[self.Y_MIN_IDX],
            y_max_bound=field_bound[self.Y_MAX_IDX],
        )
        self._right_paddle: Paddle = Paddle(
            x=self._right_paddle_initial_pos[0],
            y=self._right_paddle_initial_pos[1],
            width=paddle_width,
            height=paddle_height,
            velocity_x=0,
            velocity_y=0,
            x_min_bound=field_bound[self.X_MIN_IDX],
            x_max_bound=field_bound[self.X_MAX_IDX],
            y_min_bound=field_bound[self.Y_MIN_IDX],
            y_max_bound=field_bound[self.Y_MAX_IDX],
        )
        self._paddle_speed: int = paddle_speed // self._fps

        self._max_score: int = max_score
        self._left_paddle_score: int = 0
        self._right_paddle_score: int = 0

        self._on_start: Callable[[], None] = on_start
        self._on_turn_over: Callable[[], None] = on_turn_over
        self._on_end: Callable[[], None] = on_end

        self._is_paused: bool = False
        self._pause_lock = asyncio.Lock()

        self._is_shutdown: bool = False
        self._shutdown_lock = asyncio.Lock()

        self._is_turn_over: bool = False

        self._paddle_velocity_lock = asyncio.Lock()

        self._loop_game_task: asyncio.Task | None = None

    def start(self):
        if self._loop_game_task is not None:
            return
        self._on_start()
        self._loop_game_task = asyncio.create_task(self._loop_game())

    async def pause(self):
        if self._loop_game_task is None:
            return
        async with self._pause_lock:
            self._is_paused = True

    async def resume(self):
        if self._loop_game_task is None:
            return
        if self._is_turn_over:
            self._is_turn_over = False
        async with self._pause_lock:
            self._is_paused = False

    def end(self):
        if self._loop_game_task is None:
            return
        self._on_end()

    async def shutdown(self):
        if self._loop_game_task is None:
            return
        async with self._shutdown_lock:
            self._is_shutdown = True

    @property
    def state(self):
        game_state: dict = {
            "ball": [self._ball.x // self._size_magnification, self._ball.y // self._size_magnification],
            "paddle_y": [
                self._left_paddle.y // self._size_magnification,
                self._right_paddle.y // self._size_magnification,
            ],
            "score": [self._left_paddle_score, self._right_paddle_score],
        }
        if self._loop_game_task is None:
            return {
                "state": self.State.NOT_STARTED,
            } | game_state
        if self._get_is_game_over():
            return {
                "state": self.State.ENDED,
                "ball": [
                    self._initial_ball_pos[0] // self._size_magnification,
                    self._initial_ball_pos[0] // self._size_magnification,
                ],
                "paddle_y": [
                    self._left_paddle_initial_pos[1] // self._size_magnification,
                    self._right_paddle_initial_pos[1] // self._size_magnification,
                ],
                "score": [self._left_paddle_score, self._right_paddle_score],
            }
        if self._is_turn_over:
            return {
                "state": self.State.TURN_OVER,
            } | game_state
        if self._get_is_paused():
            return {
                "state": self.State.PAUSED,
            } | game_state
        return {
            "state": self.State.STARTED,
        } | game_state

    async def move_paddle(self, directions: tuple[str, str]) -> None:
        """
        Move paddles
        input:
            directions: tuple[str, str] - left and right paddle direction, "u", "d", "n"
        """
        left_paddle_direction, right_paddle_direction = directions
        await self._set_paddle_direction(self._left_paddle, left_paddle_direction)
        await self._set_paddle_direction(self._right_paddle, right_paddle_direction)

    # --------------------------------------------------------------------------
    #  Private methods
    # --------------------------------------------------------------------------
    async def _loop_game(self) -> None:
        while not self._get_is_game_over() and not self._get_is_shutdown():
            start_time: float = time.perf_counter()
            if not self._get_is_paused():
                await self._update_game_state()
            await self._sleep(self._frame_time - (time.perf_counter() - start_time))
        self.end()

    @staticmethod
    async def _sleep(seconds: float) -> None:
        start_time: float = time.perf_counter()
        await asyncio.sleep(seconds * 0.8)
        while time.perf_counter() - start_time < seconds:
            continue

    async def _update_game_state(self) -> None:
        self._check_collision_future()
        if await self._check_collision_ball_vertical_wall_future():
            return
        self._left_paddle.move()
        self._right_paddle.move()
        self._ball.move()

    def _check_collision_future(self) -> None:
        self._check_collision_ball_horizontal_wall_future()
        self._check_collision_ball_paddle_future()

    def _check_collision_ball_horizontal_wall_future(self) -> None:
        if self._ball.is_out_of_y_bound_future():
            self._ball.set_velocity(self._ball.velocity[0], -self._ball.velocity[1])

    async def _check_collision_ball_vertical_wall_future(self) -> bool:
        if not self._ball.is_out_of_x_bound_future():
            return False
        if self._ball.is_less_than_x_min_bound_future():
            self._right_paddle_score += 1
        elif self._ball.is_greater_than_x_max_bound_future():
            self._left_paddle_score += 1
        self._init_ball_state()
        self._init_paddles_state()
        await self.pause()
        self._is_turn_over = True
        self._on_turn_over()
        return True

    def _check_collision_ball_paddle_future(self) -> None:
        self._check_collision_ball_left_paddle_future()
        self._check_collision_ball_right_paddle_future()

    def _check_collision_ball_left_paddle_future(self) -> None:
        if (
            self._ball.x_future - self._ball.radius > self._left_paddle.x_future + self._paddle_half_width
            or self._ball.x_future < self._left_paddle.x_future - self._paddle_half_width
        ):
            return
        dist_y: int = int(abs(self._ball.y_future - self._left_paddle.y_future))
        if dist_y < self._paddle_half_height:
            self._ball.set_velocity(-self._ball.velocity[0], self._ball.velocity[1])
        elif dist_y < self._paddle_half_height + self._ball.radius:
            self._ball.set_velocity(-self._ball.velocity[0], -self._ball.velocity[1])

    def _check_collision_ball_right_paddle_future(self) -> None:
        if (
            self._ball.x_future + self._ball.radius < self._right_paddle.x_future - self._paddle_half_width
            or self._ball.x_future > self._right_paddle.x_future + self._paddle_half_width
        ):
            return
        dist_y: int = int(abs(self._ball.y_future - self._right_paddle.y_future))
        if dist_y < self._paddle_half_height:
            self._ball.set_velocity(-self._ball.velocity[0], self._ball.velocity[1])
        elif dist_y < self._paddle_half_height + self._ball.radius:
            self._ball.set_velocity(-self._ball.velocity[0], -self._ball.velocity[1])

    def _get_is_game_over(self) -> bool:
        return self._left_paddle_score >= self._max_score or self._right_paddle_score >= self._max_score

    def _get_is_shutdown(self) -> bool:
        return self._is_shutdown

    def _get_is_paused(self) -> bool:
        return self._is_paused

    def _init_ball_state(self) -> None:
        self._ball.set_position(*self._initial_ball_pos)
        ball_velocity_x, ball_velocity_y = self._get_ball_initial_velocity()
        self._ball.set_velocity(ball_velocity_x, ball_velocity_y)

    def _init_paddles_state(self) -> None:
        self._left_paddle.set_position(*self._left_paddle_initial_pos)
        self._right_paddle.set_position(*self._right_paddle_initial_pos)
        self._left_paddle.set_velocity(0, 0)
        self._right_paddle.set_velocity(0, 0)

    def _get_ball_initial_velocity(self) -> tuple[int, int]:
        ball_direction = random.uniform(0.349066, 0.872665)  # 20 ~ 50 degree
        ball_velocity_x = int(random.choice([-1, 1]) * np.cos(ball_direction) * self._ball_speed)
        ball_velocity_y = int(random.choice([-1, 1]) * np.sin(ball_direction) * self._ball_speed)
        return ball_velocity_x, ball_velocity_y

    async def _set_paddle_direction(self, paddle: Paddle, direction: str) -> None:
        async with self._paddle_velocity_lock:
            if direction == "u":
                paddle.set_velocity(0, self._paddle_speed)
            elif direction == "d":
                paddle.set_velocity(0, -self._paddle_speed)
            elif direction == "n":
                paddle.set_velocity(0, 0)
            else:
                raise ValueError("direction must be 'u', 'd', or 'n'")


class PongGameManager:
    class BallSpeed(Enum):
        SLOW = 500
        NORMAL = 1000
        FAST = 1500

    class PaddleSpeed(Enum):
        SLOW = 500
        NORMAL = 1000
        FAST = 1500

    def __init__(
        self,
        ball_speed: BallSpeed = BallSpeed.NORMAL,  # grid per second
        paddle_speed: PaddleSpeed = PaddleSpeed.NORMAL,  # grid per second
        max_score: int = 15,
        wait_delay: int = 3,
    ):
        self._game_engine: PongGameEngine = PongGameEngine(
            ball_speed=ball_speed.value,
            paddle_speed=paddle_speed.value,
            max_score=max_score,
        )
        self._wait_delay: int = wait_delay
        self._remaining_delay: int = wait_delay

        self._game_engine_state: dict = {}

    async def move_paddle(self, directions: tuple[str, str]) -> None:
        await self._game_engine.move_paddle(directions)

    async def shutdown(self):
        await self._game_engine.shutdown()

    async def game_loop(self):
        """
        이 메소드는 게임 루프를 나타냅니다.
        게임 루프는 게임이 종료될 때까지 계속해서 반복됩니다.
        """
        self._remaining_delay = self._wait_delay
        while self._remaining_delay > 0:
            await asyncio.sleep(1)
            self._remaining_delay -= 1

        self._game_engine.start()
        is_turn_over: bool = False
        while True:
            self._game_engine_state = self._game_engine.state
            if self._game_engine_state["state"] == PongGameEngine.State.TURN_OVER:
                if not is_turn_over:
                    is_turn_over = True
                    self._remaining_delay = 3
                elif self._remaining_delay == 0:
                    is_turn_over = False
                    await self._game_engine.resume()
                else:
                    await asyncio.sleep(1)
                    self._remaining_delay -= 1
                continue

            if self._game_engine_state["state"] == PongGameEngine.State.ENDED:
                break
            await asyncio.sleep(0.1)

    def get_game_state(self) -> dict:
        wait_state = 2
        if self._game_engine_state["state"] == PongGameEngine.State.TURN_OVER:
            wait_state = 1
        elif self._game_engine_state["state"] == PongGameEngine.State.STARTED:
            wait_state = 0

        ret: dict = {
            "type": "games.state",
            "finish": self._game_engine_state["state"] == PongGameEngine.State.ENDED,
            "bar": self._game_engine_state["paddle_y"],
            "ball": self._game_engine_state["ball"],
            "score": self._game_engine_state["score"],
            "wait": [wait_state, self._remaining_delay],
        }
        return ret
