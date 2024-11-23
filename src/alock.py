import threading
import asyncio
import concurrent.futures
from contextlib import asynccontextmanager

_pool = concurrent.futures.ThreadPoolExecutor()

@asynccontextmanager
async def async_lock(lock: threading.Lock):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(_pool, lock.acquire)
    try:
        yield  # the lock is held
    finally:
        lock.release()