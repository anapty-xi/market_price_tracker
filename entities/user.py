from pydantic import BaseModel
from product import Product

class User(BaseModel):
    tg_id: str
    tracking_list: list[Product]