import asyncio
import sys
from contextlib import suppress
from asynccmd import Cmd


async def sleep_n_print(loop, time_to_sleep=None):
    """
    This is our simple coroutine.
    :param time_to_sleep: time to sleep in seconds
    :return: await sleep for time_to_sleep seconds
    """
    asyncio.set_event_loop(loop)  # set correct event loop
    await asyncio.sleep(int(time_to_sleep))
    print("Wake up! I was slept for {0}s".format(time_to_sleep))


class Commander(Cmd):

    def __init__(self, intro, prompt):
        super().__init__(mode=mode)
        self.intro = intro
        self.prompt = prompt
        self.loop = None

    def do_sleep(self, arg):
        """
        Our example cmd-command-method for sleep. sleep <arg>
        :param arg: contain args that go after command
        :return: None
        """
        self.loop.create_task(sleep_n_print(self.loop, arg))

    def do_tasks(self, arg):
        """
        Our example method. Type "tasks <arg>"
        :param arg: contain args that go after command
        :return: None
        """
        for task in asyncio.Task.all_tasks(loop=self.loop):
            print(task)

    def start(self, loop=None):
        self.loop = loop
        super().cmdloop(loop)


if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    mode = "Run"
else:
    loop = asyncio.get_event_loop()
    mode = "Reader"
# asyncio.set_event_loop(loop)
cmd = Commander(intro="This is example", prompt="example> ")
cmd.start(loop)
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.stop()
    pending = asyncio.Task.all_tasks(loop=loop)
    for task in pending:
        task.cancel()
        with suppress(asyncio.CancelledError):
            loop.run_until_complete(task)
    loop.close()
