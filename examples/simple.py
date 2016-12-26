import asyncio
import sys
from asynccmd import Cmd

class SimpleCommander(Cmd):
    def __init__(self, mode, intro, prompt):
        super().__init__(mode=mode)
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
        print(super().mode)

if sys.platform == 'win32':
   loop = asyncio.ProactorEventLoop()
   mode = "Run"
else:
   loop = asyncio.get_event_loop()
   mode = "Reader"
cmd = SimpleCommander(mode=mode, intro="This is example", prompt="example> ")
cmd.start(loop)
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.stop()
