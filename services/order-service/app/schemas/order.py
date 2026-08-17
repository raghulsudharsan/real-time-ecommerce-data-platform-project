from uuid import UUID

from pydantic import BaseModel, Field
from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]  = Field(min_length=1)

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderResponse(BaseModel):
    id: UUID
    customer_id: UUID
    status: OrderStatus
    total_amount: float
    items: list[OrderItemCreate]

    class Config:
        orm_mode = True