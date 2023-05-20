import string
import random
import base64
import time

from urllib.parse import urlparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from playwright.async_api._generated import Route, Request, Browser, Playwright

def get_random_int(a: int, b: int):
    min_val = min(a, b)
    max_val = max(a, b)
    diff = max_val - min_val + 1
    return min_val + random.randint(0, diff - 1)

class Signer:
    def __init__(
        self,
        default_url="https://www.tiktok.com/@rihanna?lang=en",
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/98.0.4758.109 Safari/537.36",
        playwright=None
    ):
        self.page = None
        self.default_url = default_url
        self.user_agent = user_agent
        self.args = [
            "--disable-blink-features",
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--window-size=1920,1080",
            "--start-maximized",
            f"--user-agent='{self.user_agent}'"
        ]
        self.password = "webapp1.0+202106"
        self.playwright = playwright

        self.options = {
            "headless": True,
            "args": self.args,
        }
        self.browser: Browser | None = None

    async def init(self):
        self.browser = await self.playwright.chromium.launch(**self.options)
        emulate_template = {
            **self.playwright.devices["iPhone 11"],
            "device_scale_factor": get_random_int(1, 3),
            "is_mobile": random.random() > 0.5,
            "has_touch": random.random() > 0.5,
            "user_agent": self.user_agent
        }
        emulate_template["viewport"]["width"] = get_random_int(320, 1920)
        emulate_template["viewport"]["height"] = get_random_int(320, 1920)
        context = await self.browser.new_context(
            bypass_csp=True,
            **emulate_template
        )
        self.page = await context.new_page()

        async def route_handler(route: Route, request: Request):
            if request.resource_type == "script":
                await route.abort()
            else:
                await route.continue_()
        await self.page.route("**/*", route_handler)
        await self.page.goto(
            url=self.default_url,
            wait_until="networkidle"
        )
        load_scripts = ["signer.js", "webmssdk.js", "xbogus.js"]
        for script in load_scripts:
            await self.page.add_script_tag(path=f"./javascript/{script}")
        await self.page.evaluate('''() => {
            window.generateSignature = function generateSignature(url) {
                if (typeof window.byted_acrawler.sign !== "function") {
                    throw "No signature function found";
                }
                return window.byted_acrawler.sign({ url: url });
            };
            window.customGenerateBogus = function(params) {
                if (typeof window.generateBogus !== "function") {
                    throw "No X-Bogus function found";
                }
                return window.generateBogus(params);
            };
            return this;
        }''')

    async def navigator(self):
        info = await self.page.evaluate('''() => {
            return {
                deviceScaleFactor: window.devicePixelRatio,
                user_agent: window.navigator.userAgent,
                browser_language: window.navigator.language,
                browser_platform: window.navigator.platform,
                browser_name: window.navigator.appCodeName,
                browser_version: window.navigator.appVersion,
            };
        }''')
        return info

    @staticmethod
    def generatevfp():
        verify_fp = 'verify_5b161567bda98b6a50c0414d99909d4b'  # !!! NOT SURE IF EXPIRE
        if verify_fp:
            return verify_fp

    async def sign(self, link: str):
        verify_fp = self.generatevfp()
        new_url = f"{link}&verifyFp={verify_fp}"
        _signature = await self.page.evaluate(f'generateSignature("{new_url}")')
        signed_url = new_url + "&_signature" + _signature
        query_string = urlparse(signed_url).query
        bogus = await self.page.evaluate(f'generateBogus("{query_string}","{self.user_agent}")')
        signed_url += "&X-Bogus=" + bogus
        return {
            "signature": _signature,
            "verify_fp": verify_fp,
            "signed_url": signed_url,
            "x-tt-params": self.xttparams(query_string),
            "x-bogus": bogus,
            "navigator": await self.navigator()
        }

    def xttparams(self, query_str):
        query_str += "&is_encryption=1"
        password = self.password.ljust(16, '\0')
        query_bytes = query_str.encode('utf-8')
        padded_query_bytes = pad(query_bytes, 16)
        cipher = AES.new(password.encode(), AES.MODE_CBC, password.encode())
        encrypted = cipher.encrypt(padded_query_bytes)
        return base64.b64encode(encrypted).decode('utf-8')
