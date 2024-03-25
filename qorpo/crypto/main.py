from api import main_app_factory
from db import init_db

from aiohttp import web

if __name__ == "__main__":
    init_db()
    web.run_app(main_app_factory(), port=8000)
