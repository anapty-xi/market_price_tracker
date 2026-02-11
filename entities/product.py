from pydantic import BaseModel, Field, AfterValidator, ValidationError
from decimal import Decimal
from typing import Annotated

def is_real_url(url):
    if url.startswith("https://market.yandex.ru/card/"):
        return url
    raise ValidationError(f'{url} is not correct ymarket url')

class Product(BaseModel):
    name: str
    price: Annotated[Decimal, Field(ge=0)]
    url: Annotated[str, AfterValidator(is_real_url)]
    available: bool

