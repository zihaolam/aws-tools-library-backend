from asyncio import get_event_loop
from typing import Callable, List


def run_async(*funcs: List[Callable]):
    loop = get_event_loop()
    return loop.run_until_complete(funcs)
