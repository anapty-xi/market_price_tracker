from fastapi import APIRouter, HTTPException, status, Depends, Body
from typing import Annotated
from datetime import date
from decimal import Decimal

from api import dependencies
from entities.product import Product
from usecases.product.product_usecases import GetProductPriceChange, GetProductsInformation

router = APIRouter()


@router.get('/products/card-info')
async def get_products_info(tg_id: Annotated[int, Depends(dependencies.user_tg_id)],
                            usecase: Annotated[GetProductsInformation, Depends(dependencies.get_products_info_usecase)]) -> list[Product]:
    products = await usecase.execute(tg_id)
    return products

@router.get('products/price-track')
async def get_price_track(tg_id: Annotated[int, Depends(dependencies.user_tg_id)],
                          usecase: Annotated[GetProductPriceChange, Depends(dependencies.product_price_changes_usecase)],
                          product_url: Annotated[str, Body()]) -> dict[date, Decimal]:
    try:
        track = await usecase.execute(product_url)
        return track
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail='DB error')