from typing import Protocol
from decimal import Decimal
from datetime import date

class ProductProtocol(Protocol):
    def get_products_data(self, products_urls: list[str]) -> list[dict[str, str | Decimal]]:
        pass
    def get_product_price_change(self, product_url: str) -> dict[date, Decimal]:
        pass