from sqlalchemy import func, select, desc
from sqlalchemy.orm import Session

from db import ENGINE
from apps.price.config import PAGE_SIZE
from apps.price.models import Currencies


class TestHistory:
    def currencies_count(self):
        with Session(ENGINE) as session:
            return session.query(func.count(Currencies.id)).scalar()
        
    async def test_delete_history(self, client, fill_db):
        resp = await client.delete("/history")
        assert resp.status == 200
        assert self.currencies_count() == 0

    async def test_get_page(self, client, fill_db):
        resp = await client.get("/history", params={"page": 1})
        assert resp.status == 200

        with Session(ENGINE) as session:
            query = select(Currencies).limit(PAGE_SIZE).offset(0)
            records = session.query(Currencies).from_statement(query).all()
            result = [record.to_dict() for record in records]

        assert resp.content_type == "application/json"
        assert result == await resp.json()

    async def test_get_empty_page(self, client):
        resp = await client.get("/history", params={"page": 1})
        assert resp.status == 200
        
        data = await resp.json()
        assert data == []

    async def test_get_wrong_page(self, client):
        resp = await client.get("/history", params={"page": 0})
        assert resp.status == 400

        resp = await client.get("/history", params={"page": -100})
        assert resp.status == 400


class TestCurrency:
    def currencies_count(self):
        with Session(ENGINE) as session:
            return session.query(func.count(Currencies.id)).scalar()

    async def test_get_currency(self, client):
        row_count = self.currencies_count()
        resp = await client.get("/BTC")

        assert resp.status == 200
        assert self.currencies_count() == row_count + 1

        qdata = await resp.json()
        with Session(ENGINE) as session:
            result = session.query(Currencies).order_by(desc(Currencies.timestamp)).first()
        assert qdata == result.to_dict()

    async def test_get_bad_symbol(self, client):
        row_count = self.currencies_count()
        resp = await client.get("UNKNOWN_SYMBOL")
        assert resp.status == 400
        assert self.currencies_count() == row_count
