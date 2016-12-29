from aiohttp import web
import logging

logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level = logging.DEBUG)

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def wshandler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.MsgType.text:
            ws.send_str("Hello, {}".format(msg.data))
        elif msg.type == web.MsgType.binary:
            ws.send_bytes(msg.data)
        elif msg.type == web.MsgType.close:
            break

    return ws


app = web.Application()
app.router.add_get('/echo', wshandler)
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)

web.run_app(app)
