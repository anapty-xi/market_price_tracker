from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from decimal import Decimal
from datetime import date


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'User'

    tg_id: Mapped[str] = mapped_column(primary_key=True)

    product_list: Mapped[list['Product']] = relationship(back_populates='user')

class Product(Base):
    __tablename__ = 'Product'

    url: Mapped[str] = mapped_column(primary_key=True)

    user_id: Mapped[str] = mapped_column(ForeignKey('User.tg_id'))
    user: Mapped[User] = relationship(back_populates='product_list')

    price_history: Mapped[list['PriceHistory']] = relationship(back_populates='product')

class PriceHistory(Base):
    __tablename__ = 'PriceHistory'

    price_history_id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[Decimal]
    date: Mapped[date]

    product_url: Mapped[str] = mapped_column(ForeignKey('Product.url'))
    product: Mapped[Product] = relationship(back_populates='price_history')