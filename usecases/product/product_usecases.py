from product_protocol import ProductProtocol
from entities.product import Product
from decimal import Decimal
from datetime import date 

class BaseUsecase:
    def __init__(self, infrastructure: ProductProtocol):
        self.infrastructure = infrastructure()


class GetProductsInformation(BaseUsecase):
    async def execute(self, products_urls: list[str]) -> list[Product]:
        products_data = await self.infrastructure.get_products_data(products_urls)

        products_entities = []
        for product in products_data:
            if 'error' in product:
                products_entities.append(Product(
                    name='ERROR',
                    price=1,
                    url=product['url'],
                    available=False
                ))
            else:
                products_entities.append(Product(**product))
        
        return products_entities
    

class GetProductPriceChange(BaseUsecase):
    async def execute(self, product_url: str) -> dict[date, Decimal]:
        return await self.infrastructure.get_product_price_change(product_url)
