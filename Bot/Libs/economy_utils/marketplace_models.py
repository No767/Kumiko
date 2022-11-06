from typing import Optional

from beanie import Document
from pydantic import BaseModel


class MarketplaceModel(Document):
    name: str
    description: Optional[str] = None
    amount: int
    price: int
    date_added: str
    owner: int
    owner_name: str
    uuid: str
    updated_price: bool


class PurchaseProject(BaseModel):
    owner: int
    name: str
    description: str
    price: int
    amount: int
    uuid: str


class ItemAuthProject(BaseModel):
    uuid: str
