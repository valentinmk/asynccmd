import logging
#adding logging for see http requests
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level = logging.DEBUG)
logging.info("import asyncio")
import asyncio
logging.info("import sys")
import sys
logging.info("from contextlib import suppress")
from contextlib import suppress
logging.info("from aiohttp import web")
from aiohttp import web



class AiohttpCmdHelper:
    port = 8080
    loop = asyncio.get_event_loop()
    def __init__(self, loop, port):
        logging.info("__init__")
        self.loop = loop
        self.port = port

    async def handle(request):
        logging.info("handle")
        name = request.match_info.get('name', "Anonymous")
        text = "Hello, " + name
        return web.Response(text=text)

    def start(self):
        logging.info("start")
        logging.info(self.loop)
        self.app = web.Application()
        self.app.router.add_get('/', self.handle)
        self.app.router.add_get('/{name}', self.handle)
        self.handler = self.app.make_handler()
        logging.info("self.handler = {0}".format(self.handler))
        self.srv = self.loop.run_until_complete(self.loop.create_server(self.handler,
                                                                        host = '0.0.0.0',
                                                                        port = self.port))
        logging.info(self)
        logging.info("start end")

    def stop(self):
        logging.info("stop")
        self.srv.close()
        self.loop.run_until_complete(self.srv.wait_closed())
        self.loop.run_until_complete(self.app.shutdown())
        self.loop.run_until_complete(self.handler.shutdown(60.0))
        self.loop.run_until_complete(self.app.cleanup())

if sys.platform == 'win32':
   loop = asyncio.ProactorEventLoop()
   mode = "Run"
else:
   loop = asyncio.get_event_loop()
   mode = "Reader"

#asyncio.set_event_loop(loop) # set our event loop for aiohttp
test = AiohttpCmdHelper(loop=loop, port=8080)
test.start()

try:
    logging.info("3")
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    test.stop()
    loop.stop()
    pending = asyncio.Task.all_tasks(loop=loop)
    for task in pending:
        task.cancel()
        with suppress(asyncio.CancelledError):
            loop.run_until_complete(task)
loop.close()
