from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column

from models import Base


class Currencies(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    currency: Mapped[str] = mapped_column(String(30))
    timestamp: Mapped[datetime] = mapped_column("date_")
    price: Mapped[float]

    def __repr__(self):
        return f"Currencies(currency={self.currency}, timestamp={self.timestamp}, price={self.price})"

    def to_dict(self):
        return {
            "currency": self.currency,
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "price": self.price,
        }
