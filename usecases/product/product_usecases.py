from usecases.product.product_protocol import ProductDBProtocol, ProductParserProtocol
from entities.product import Product
from decimal import Decimal
from datetime import date 

class BaseUsecase:
    def __init__(self, db_infrastructure: ProductDBProtocol, parser_infrastructure: ProductParserProtocol | None = None):
        self.db_infrastructure = db_infrastructure()
        self.parser_infrastructure = parser_infrastructure()

class ParseProductsData(BaseUsecase):
    async def execute(self, tg_id: str) -> list[Product]:
        if not await self.db_infrastructure.is_user_exists(tg_id):
            raise ValueError('User does not exist')
        products_urls = await self.db_infrastructure.get_tracking_list(tg_id)
        if products_urls:
            products_data = await self.parser_infrastructure.parse_products_data(products_urls)
        else:
            return []
        
        products_entities = []
        for product in products_data:
            products_entities.append(Product(**product))

        return products_entities
    

class GetProductPriceTrack(BaseUsecase):
    async def execute(self, product_url: str) -> dict[date, Decimal]:
        return await self.db_infrastructure.get_product_price_track(product_url)
    

class ParseAllProductsForDB(BaseUsecase):
    async def execute(self) -> None:
        products_urls = await self.db_infrastructure.get_tracking_list(tg_id=None)
        if products_urls:
            products_data = await self.parser_infrastructure.parse_products_data(products_urls)
        else:
            return None
        
        await self.db_infrastructure.save_new_price_data(products_data)