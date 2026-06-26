from decimal import Decimal
from enum import Enum
from uuid import UUID

from sqlalchemy import Enum as SQLEnum, Numeric
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.models.base import BaseModel


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class Order(BaseModel):
    __tablename__ = "orders"
    customer_id: Mapped[UUID] = mapped_column(
    nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
    SQLEnum(OrderStatus),
    default=OrderStatus.PENDING)
    total_amount: Mapped[Decimal] = mapped_column(
    Numeric(10, 2))
    items: Mapped[list["OrderItem"]] = relationship(
    back_populates="order",
    cascade="all, delete-orphan",
)