# Copyright (c) 2016-present Valentin Kazakov
#
# This module is part of asyncpg and is released under
# the Apache 2.0 License: http://www.apache.org/licenses/LICENSE-2.0

import asyncio
import gc
import pytest
import concurrent.futures
from asynccmd import Cmd
from contextlib import suppress


@pytest.yield_fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    executor = concurrent.futures.ThreadPoolExecutor()
    loop.set_default_executor(executor)
    yield loop

    if loop.is_closed:
        pending = asyncio.Task.all_tasks(loop=loop)
        for task in pending:
            task.cancel()
            # Now we should await task to execute it's cancellation.
            # Cancelled task raises asyncio.CancelledError that we can suppress
            with suppress(asyncio.CancelledError):
                loop.run_until_complete(task)
        executor.shutdown()
        loop.close()

    gc.collect()
    asyncio.set_event_loop(None)


@pytest.fixture
def aio_cmd(loop, mode):
    aio_cmd = Cmd(mode=mode, run_loop=False)
    aio_cmd.cmdloop(loop)
    return aio_cmd
