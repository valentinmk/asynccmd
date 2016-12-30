import logging
import asyncio
import sys

from contextlib import suppress
from aiohttp import web
from asynccmd import Cmd

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s '
                    '[%(asctime)s]  %(message)s',
                    level=logging.DEBUG)  # just for visualisation


class AiohttpCmdHelper:
    """
    Helper class that do all aiohttp start stop manipulation
    """
    port = 8080  # Default port
    loop = None  # By default loop is not set

    def __init__(self, loop, port):
        self.loop = loop
        self.port = port

    async def handle(self, request):
        """
        Simple handler that answer http request get with port and name
        """
        name = request.match_info.get('name', "Anonymous")
        text = 'Aiohttp server running on {0} port. Hello, {1}'.format(
            str(self.port), str(name))
        return web.Response(text=text)

    async def start(self):
        """
        Start aiohttp web server
        """
        self.app = web.Application()
        self.app.router.add_get('/', self.handle)
        self.app.router.add_get('/{name}', self.handle)
        self.handler = self.app.make_handler()
        self.f = self.loop.create_server(self.handler,
                                         host='0.0.0.0',
                                         port=self.port)
        # Event loop is already runing, so we await create server instead
        # of run_until_complete
        self.srv = await self.f

    async def stop(self):
        """
        Stop aiohttp server
        """
        self.srv.close()
        await self.srv.wait_closed()
        await self.app.shutdown()
        await self.handler.shutdown(60.0)
        await self.app.cleanup()


class Commander(Cmd):
    """
    Our main example with new start and stop cli command
    :param aiohttp_servers: store all instances of AiohttpCmdHelper class
    """
    aiohttp_servers = []

    def __init__(self, intro, prompt):
        super().__init__(mode=mode)
        self.intro = intro
        self.prompt = prompt
        self.loop = None

    def do_start(self, arg):
        """
        Our example cli-command-method for start aiohttp server. start <arg>
        :param arg: Port number
        :return: None
        """
        if not arg:  # we use simple check in our demonstration
            print("Error port is empty")
        else:
            test = AiohttpCmdHelper(loop=self.loop, port=int(arg))
            self.aiohttp_servers.append({test, int(arg)})
            self.loop.create_task(test.start())

    def do_stop(self, arg):
        """
        Our example cli-command-method for stop aiohttp server. start <arg>
        :param arg: Port number
        :return: None
        """
        if not arg:  # we use simple check in our demonstration
            print("Error! Provided port is empty")
        else:
            aiohttp_servers = []
            for port, server in self.aiohttp_servers:
                print('server = {0}, port = {1}'.format(server, port))
                if port == int(arg):
                    self.loop.create_task(server.stop())
                else:
                    aiohttp_servers.append({server, port})
            self.aiohttp_servers = aiohttp_servers

    def do_tasks(self, arg):
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

asyncio.set_event_loop(loop)  # set our event loop for aiohttp (fix for Win32)
cmd = Commander(intro="This is example", prompt="example> ")
cmd.start(loop)
try:
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
