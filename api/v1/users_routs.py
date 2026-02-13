from fastapi import APIRouter, HTTPException, status, Depends, Body
from typing import Annotated

from api import dependencies
from entities.user import User
from usecases.user.user_usecases import GetProductList, ProductListOperations

router = APIRouter()


@router.get('/products')
async def get_user_products_list(tg_id: Annotated[int, Depends(dependencies.user_tg_id)], 
                                 usecase: Annotated[GetProductList, Depends(dependencies.get_pl_usecase)]) -> User:
    user = await usecase.execute(tg_id)
    if isinstance(user, User):
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

@router.post('/products')
async def add_product_in_list(tg_id: Annotated[int, Depends(dependencies.user_tg_id)], 
                              product_url: Annotated[str, Body()],
                              usecase: Annotated[ProductListOperations, Depends(dependencies.pl_operations_usecase)]) -> dict[str, str]:
    if await usecase.execute(tg_id, product_url, add=True):
        return {'added': f'{product_url}'}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) 

@router.delete('/products')
async def delete_post_in_list(tg_id: Annotated[int, Depends(dependencies.user_tg_id)], 
                              product_url: Annotated[str, Body()],
                              usecase: Annotated[ProductListOperations, Depends(dependencies.pl_operations_usecase)]) -> dict[str, str]:
    if await usecase.execute(tg_id, product_url, delete=True):
        return {'deleted': f'{product_url}'}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) 