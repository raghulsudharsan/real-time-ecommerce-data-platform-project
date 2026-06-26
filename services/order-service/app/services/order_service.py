from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate


class OrderService:

    def __init__(self,repository: OrderRepository,):
        self.repository = repository

    def create_order(
        self,
        db: Session,
        request: OrderCreate,
    ) -> Order:

        total_amount = Decimal("0.00")

        order = Order(
            customer_id=request.customer_id,
            status=OrderStatus.PENDING,
            total_amount=total_amount,
        )

        try:

            order = self.repository.create_order(
                db=db,
                order=order,
            )

            for item in request.items:

                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                )

                self.repository.create_order_item(
                    db=db,
                    order_item=order_item,
                )

            db.commit()

            return order

        except Exception:

            db.rollback()

            raise