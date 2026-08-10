from pydantic import BaseModel, ConfigDict, Field 
from decimal import Decimal
from uuid import UUID
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: Decimal
    brand:str | None = None
    storage:str | None = None
    color:str | None = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductUpdate(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    brand:str | None = None
    storage:str | None = None
    color:str | None = None

class ProductBulkRequest(BaseModel):
    product_ids: list[UUID] = Field(min_length=1)
