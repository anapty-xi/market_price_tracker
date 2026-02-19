from fastapi import APIRouter, HTTPException, status, Depends, Body
from typing import Annotated
from datetime import date
from decimal import Decimal
from loguru import logger

from api import dependencies
from entities.product import Product
from usecases.product.product_usecases import ParseProductsData, GetProductPriceTrack

router = APIRouter()


@router.get('/products_data')
async def parse_products_data(tg_id: Annotated[str, Depends(dependencies.user_tg_id)],
                              usecase: Annotated[ParseProductsData, Depends(dependencies.parse_product_data_usecase)]) -> list[Product]:
    try:
        products_entities = await usecase.execute(tg_id)
        logger.success(f'User {tg_id} parsed products data')
        return products_entities
    
    except ValueError:
        logger.error('User not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    


@router.get('/price_track')
async def get_product_price_track(product_url: str,
                                  usecase: Annotated[GetProductPriceTrack, Depends(dependencies.get_products_price_track)]) -> dict[date, Decimal]:
    try:
        price_track = await usecase.execute(product_url)
        logger.success(f'Product {product_url} price track returned')
        return price_track
    
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product no found')

