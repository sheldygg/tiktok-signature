import asyncio

from urllib.parse import urlencode
from tiktok_signature import Signer
from playwright.async_api import async_playwright

# pip install aiotiktok
from aiotiktok import Client
from aiotiktok.constants import static_user_videos_url, static_unsigned_user_videos, default_user_videos_params

from request import make_request


async def main():
    uid = (await Client().user_info("therock")).sec_uid
    params = default_user_videos_params
    params.update({"secUid": uid})
    playwright = await async_playwright().start()
    try:
        signer = Signer(playwright=playwright)
        await signer.init()
        unsigned_url = f"{static_unsigned_user_videos}{urlencode(params)}"
        signature_data = await signer.sign(unsigned_url)
        headers = {
            "x-tt-params": signature_data.get("x-tt-params"),
            "user-agent": signature_data.get("navigator", {}).get("user_agent"),
        }
        response = (await make_request(static_user_videos_url, headers)).json()
        print(response)

    finally:
        await playwright.stop()


asyncio.run(main())
