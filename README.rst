####################
tiktok-signature
####################

.. image:: https://img.shields.io/pypi/v/tiktok-signature?color=blue
    :target: https://pypi.python.org/pypi/tiktok-signature
    :alt: PyPi Package Version

.. image:: https://img.shields.io/pypi/dm/tiktok-signature?color=blue
    :target: https://pypi.python.org/pypi/tiktok-signature
    :alt: Downloads

Server
========

.. code-block:: python

   import asyncio

   from playwright.async_api import async_playwright
   from pydantic import BaseSettings
   from tiktok_signature.server import make_server


   class Settings(BaseSettings):
       host: str
       port: int

       class Config:
           env_file = ".env"
           env_file_encoding = "utf-8"


   async def main():
       settings = Settings()
       async with async_playwright() as playwright:
           server = await make_server(playwright=playwright, host=settings.host, port=settings.port)
           await server.start()
           await asyncio.Event().wait()

   asyncio.run(main())


As package
=====
.. code-block:: python

    import asyncio

    from tiktok_signature import Signer
    from playwright.async_api import async_playwright


    async def main():
        async with async_playwright() as playwright:
            signer = Signer(playwright=playwright)
            await signer.init()
            await signer.sign("url")

    asyncio.run(main())

Docker
====
You can build image yourself

.. code-block:: rst

    docker build . -t tiktok-signature

Or start with the second command and use the ready image

.. code-block:: rst

    docker run --name=tiktok-signature --restart=always -p 8002:8002 -e port=8002 sheldygg/tiktok-signature