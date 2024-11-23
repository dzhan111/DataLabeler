import threading
import asyncio
import concurrent.futures
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_lock(lock: threading.Lock, pool: concurrent.futures.ThreadPoolExecutor):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(pool, lock.acquire)
    try:
        yield  # the lock is held
    finally:
        lock.release()