import asyncio
import sys
from contextlib import suppress
sys.path.append("..")
from asynccmd import Cmd

class Commander(Cmd):
    def __init__(self, intro, prompt):
        if sys.platform == 'win32':
            super().__init__(mode="Run", run_loop=False)
        else:
            super().__init__(mode="Reader", run_loop=False)
        self.intro = intro
        self.prompt = prompt
        self.loop = None

    def do_tasks(self, arg):
        """
        Fake command. Type "tasks {arg}"
        :param arg: args occurred from cmd after command
        :return:
        """
        print(asyncio.Task.all_tasks(loop=self.loop))

    def start(self, loop=None):
        self.loop = loop
        super().cmdloop(loop)

if sys.platform == 'win32':
   loop = asyncio.ProactorEventLoop()
else:
   loop = asyncio.get_event_loop()
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
