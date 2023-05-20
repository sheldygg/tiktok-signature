import asyncio

from aiohttp.web import Application, TCPSite, AppRunner, json_response
from aiohttp.web_request import Request
from playwright.async_api import async_playwright
from signature import Signer


async def get_request(request: Request):
    return json_response({"ok": True, "ip": request.remote})


async def post_request(request: Request):
    signer: Signer = request.app["signer"]
    post_data = await request.post()
    return json_response(await signer.sign(post_data.get("url")))


async def main():
    playwright = await async_playwright().start()
    try:
        signer = Signer(playwright=playwright)
        await signer.init()
        app = Application()
        app["signer"] = signer
        app.router.add_post(
            path="/signature", handler=post_request
        )
        app.router.add_get(
            path="", handler=get_request
        )
        runner = AppRunner(app)
        await runner.setup()
        site = TCPSite(runner, host="127.0.0.1", port=8080)
        await site.start()
        await asyncio.Event().wait()
    finally:
        await playwright.stop()


asyncio.run(main())
