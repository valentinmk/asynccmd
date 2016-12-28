import asyncio
import gc
import pytest
import sys
import concurrent.futures
from asynccmd import Cmd
from contextlib import suppress

@pytest.yield_fixture
def loop():
    #print("conftest loop start")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    executor = concurrent.futures.ThreadPoolExecutor()
    loop.set_default_executor(executor)
    #print("conftest loop = {0}".format(loop))
    #print("conftest yield loop")
    yield loop

    #print("conftest loop closing")
    if loop.is_closed:
        #print("++++++++++++++++++++++++++++++++++++++++++++loop.is_closed")
        pending = asyncio.Task.all_tasks(loop=loop)
        for task in pending:
            #print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{0}".format(task))
            task.cancel()
            # Now we should await task to execute it's cancellation.
            # Cancelled task raises asyncio.CancelledError that we can suppress:
            with suppress(asyncio.CancelledError):
                loop.run_until_complete(task)
        executor.shutdown()
        loop.close()

    #print("conftest gc")
    gc.collect()
    #print("conftest set None")
    asyncio.set_event_loop(None)

@pytest.fixture
def aio_cmd(loop, mode):
    aio_cmd = Cmd(mode=mode, run_loop=False)
    aio_cmd.cmdloop(loop)
    return aio_cmd
