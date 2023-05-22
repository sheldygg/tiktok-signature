from aiohttp.web import Application, AppRunner, TCPSite, json_response
from aiohttp.web_request import Request

from .signature import Signer


async def get_request(request: Request):
    return json_response({"ok": True, "ip": request.remote})


async def post_request(request: Request):
    signer: Signer = request.app["signer"]
    post_data = await request.post()
    url = post_data.get("url")
    return json_response(await signer.sign(url))


async def make_server(playwright, host: str, port: int):
    signer = Signer(playwright=playwright)
    await signer.init()
    app = Application()
    app["signer"] = signer
    app.router.add_post(path="/signature", handler=post_request)
    app.router.add_get(path="", handler=get_request)
    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, host=host, port=port)
    return site
