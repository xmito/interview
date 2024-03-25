from apps.price.api import price_app
from db import init_db

from aiohttp import web

async def main_app_factory():
    main_app = web.Application()
    main_app.add_subapp('/price', price_app)
    return main_app
