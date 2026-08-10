from decimal import Decimal
from fastapi import HTTPException
from uuid import UUID
from httpcore import request
from sqlalchemy.orm import Session

from app.kafka.producer import KafkaProducer
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate
from app.clients.product_client import ProductClient


class OrderService:

    def __init__(
        self,
        repository: OrderRepository,
    ):
        self.repository = repository
        self.product_client = ProductClient()
        self.kafka_producer = KafkaProducer()


    ALLOWED_TRANSITIONS = {
    OrderStatus.PENDING: {
        OrderStatus.CONFIRMED,
        OrderStatus.CANCELLED,
    },
    OrderStatus.CONFIRMED: {
        OrderStatus.PAID,
        OrderStatus.CANCELLED,
    },
    OrderStatus.PAID: {
        OrderStatus.SHIPPED,
    },
    OrderStatus.SHIPPED: {
        OrderStatus.DELIVERED,
    },
    OrderStatus.DELIVERED: set(),
    OrderStatus.CANCELLED: set(),
}
    def create_order(
        self,
        db: Session,
        request: OrderCreate,
    ) -> Order:

        product_ids = [item.product_id for item in request.items]
        products = self.product_client.get_products(product_ids)
        products_by_id = {UUID(product["id"]): product for product in products}
        order = Order(
    customer_id=request.customer_id,
    status=OrderStatus.PENDING,
    total_amount=Decimal("0.00"),
    )
        
        for item in request.items:
            product = products_by_id.get(item.product_id)
            if not product:
                raise ValueError(f"Product with ID {item.product_id} not found.")
            order_item = OrderItem(
            product_id=item.product_id,
            product_name=product["name"],
            unit_price=Decimal(str(product["price"])),
            quantity=item.quantity,
            subtotal=Decimal(str(product["price"])) * item.quantity,
)
            order.items.append(order_item)
            order.total_amount += order_item.subtotal

        self.repository.create_order(db, order)
        self.kafka_producer.publish({"order_id": str(order.id)})
        return order

    def get_order_by_id(self, db: Session, order_id: UUID) -> Order | None:
        order =  self.repository.get_order_by_id(db, order_id)
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    def get_all_orders(self, db: Session) -> list[Order]:
        return self.repository.get_all_orders(db)

    def update_order_status(self, db: Session, order_id: UUID, request: OrderStatus) -> Order:
        order = self.repository.get_order_by_id(
        db=db,
        order_id=order_id,
    )
        if request.status not in self.ALLOWED_TRANSITIONS[order.status]:
            raise HTTPException(
        status_code=400,
        detail=f"Cannot change order status from {order.status} to {request.status}",
    )
        order = self.repository.update_order_status(db, order_id, request.status)

        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
        