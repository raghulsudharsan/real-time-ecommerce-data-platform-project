from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.order import Order

class OrderItem(BaseModel):
    __tablename__ = "order_items"

    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("orders.id")
    )

    product_id: Mapped[UUID] = mapped_column(nullable=False)

    product_name: Mapped[str] = mapped_column(nullable=False)

    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    quantity: Mapped[int] = mapped_column(default=1)

    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    order: Mapped["Order"] = relationship(
        back_populates="items"
    )