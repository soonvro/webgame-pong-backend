import asyncio
import time


async def async_sleep(seconds: float) -> None:
    start_time: float = time.perf_counter()
    await asyncio.sleep(seconds * 0.9)
    while time.perf_counter() - start_time < seconds:
        pass
