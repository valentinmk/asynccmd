import logging
import asyncio
import sys

from contextlib import suppress
from aiohttp import web
from asynccmd import Cmd

logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level = logging.DEBUG)

class AiohttpCmdHelper:
    port = 8080
    loop = asyncio.get_event_loop()
    def __init__(self, loop, port):
        logging.info("__init__")
        self.loop = loop
        self.port = port

    async def handle(self, request):
        logging.info("handle")
        name = request.match_info.get('name', "Anonymous")
        text = "Hello, " + name
        return web.Response(text=text)

    async def start(self):
        logging.info("start")
        logging.info(self.loop)
        self.app = web.Application()
        self.app.router.add_get('/', self.handle)
        self.app.router.add_get('/{name}', self.handle)
        self.handler = self.app.make_handler()
        logging.info("self.handler = {0}".format(self.handler))
        self.f = self.loop.create_server(self.handler,
                                         host = '0.0.0.0',
                                         port = self.port)
        self.srv = await self.f

    def stop(self):
        logging.info("stop")
        self.srv.close()
        self.loop.run_until_complete(self.srv.wait_closed())
        self.loop.run_until_complete(self.app.shutdown())
        self.loop.run_until_complete(self.handler.shutdown(60.0))
        self.loop.run_until_complete(self.app.cleanup())

class Commander(Cmd):
    def __init__(self, intro, prompt):
        super().__init__(mode=mode)
        self.intro = intro
        self.prompt = prompt
        self.loop = None

    def do_start(self, arg):
        """
        Our example cmd-command-method for sleep. sleep <arg>
        :param arg: contain args that go after command
        :return: None
        """
        if not arg:
            print("Error")
        else:
            test = AiohttpCmdHelper(loop=self.loop, port=int(arg))
            self.loop.create_task(test.start())


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

asyncio.set_event_loop(loop) # set our event loop for aiohttp
cmd = Commander(intro="This is example", prompt="example> ")
cmd.start(loop)
try:
    logging.info("3")
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.stop()
    pending = asyncio.Task.all_tasks(loop=loop)
    for task in pending:
        task.cancel()
        with suppress(asyncio.CancelledError):
            loop.run_until_complete(task)
loop.close()
