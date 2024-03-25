from datetime import timezone, datetime

import pytest
import ccxt.async_support as ccxt
from aiohttp import web
from sqlalchemy.orm import Session

from db import init_db, ENGINE
from apps.price.api import app_price_factory
from apps.price.models import Currencies


@pytest.fixture(scope="module")
def initialize_db():
    init_db()


@pytest.fixture
async def fill_db(initialize_db):
    kucoin = ccxt.kucoin()
    markets = await kucoin.load_markets()
    tickers = await kucoin.fetch_tickers(
        [symbol for symbol in markets.keys() if symbol.endswith('USDT')]
    )
    await kucoin.close()

    with Session(ENGINE) as session, session.begin():
        for symbol, ticker in tickers.items():
            currency, _ = symbol.split('/')
            timestamp = datetime.fromtimestamp(ticker['timestamp'] / 1000.0, tz=timezone.utc)

            if ticker['bid'] is None:
                continue
            entry = Currencies(currency=currency, price=ticker['bid'], timestamp=timestamp)
            session.add(entry)

    yield

    with Session(ENGINE) as session, session.begin():
        session.query(Currencies).delete()


@pytest.fixture
async def client(aiohttp_client):
    price_app = app_price_factory()
    client = await aiohttp_client(price_app)
    yield client
    await client.close()