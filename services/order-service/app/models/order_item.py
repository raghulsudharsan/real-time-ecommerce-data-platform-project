from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

class OrderItem(BaseModel):
    __tablename__ = "order_items"

    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("orders.id")
    )

    product_id: Mapped[UUID] = mapped_column(nullable=False)

    quantity: Mapped[int] = mapped_column(
    nullable=False,
    default=1)
    order: Mapped["Order"] = relationship(
        back_populates="items"
    )