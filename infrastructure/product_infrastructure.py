from usecases.product.product_protocol import ProductProtocol
from decimal import Decimal
from datetime import date

class ProductParser(ProductProtocol):
    async def get_products_data(self, products_urls: list[str]) -> list[dict[str, str | Decimal]]:
        pass

class ProductDBGateway(ProductProtocol):
    async def get_product_price_change(self, product_url: str) -> dict[date, Decimal]:
        pass