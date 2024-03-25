from datetime import datetime, timezone

import ccxt.async_support as ccxt
from aiohttp import web
from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.price.config import PAGE_SIZE
from apps.price.models import Currencies
from db import ENGINE

routes = web.RouteTableDef()

@routes.get('/history')
async def history(request):
    try:
        page = int(request.query.get('page', 1))
        if page < 1:
            return web.json_response({'error': "Invalid value for page"}, status=400)
    except ValueError:
        return web.json_response({'error': "Invalid value for page"}, status=400)

    offset = (page - 1) * PAGE_SIZE
    with Session(ENGINE) as session, session.begin():
        query = select(Currencies).limit(PAGE_SIZE).offset(offset)
        records = session.query(Currencies).from_statement(query).all()
        result = [record.to_dict() for record in records]

    return web.json_response(result)


@routes.delete('/history')
async def history(request):
    with Session(ENGINE) as session, session.begin():
        session.query(Currencies).delete()
        session.commit()

    return web.Response(text="OK", status=200)


@routes.get('/{currency}')
async def price(request):
    currency = request.match_info['currency'].upper()

    try:
        kucoin = ccxt.kucoin()
        ticker = await kucoin.fetch_ticker(f"{currency}/USDT")
        await kucoin.close()

    except ccxt.BadSymbol as ex:
        return web.Response(text=str(ex), status=400)
    except ccxt.NetworkError as ex:
        return web.Response(text=str(ex), status=503)
    except Exception as ex:
        return web.Response(text=f"Internal Server Error: {ex}", status=500)


    timestamp = datetime.fromtimestamp(ticker['timestamp'] / 1000.0, tz=timezone.utc)
    with Session(ENGINE, expire_on_commit=False) as session, session.begin():
        entry = Currencies(currency=currency, price=ticker['bid'], timestamp=timestamp)
        session.add(entry)

    return web.json_response(entry.to_dict())


def app_price_factory():
    price_app = web.Application()
    price_app.add_routes(routes)
    return price_app

price_app = app_price_factory()