from unittest import result
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem

class OrderRepository:
    def create_order(self, db: Session, order: Order) -> Order:
        db.add(order)
        db.commit()
        db.refresh(order)

        return order
    
    def create_order_item(self,db: Session,order_item: OrderItem) -> OrderItem:
        db.add(order_item)
        db.commit()
        db.refresh(order_item)

        return order_item
    
    def get_order_by_id(self,db: Session,order_id: UUID) -> Order | None:
        statement = (
        select(Order)
        .where(Order.id == order_id))

        result = db.execute(statement)

        return result.scalar_one_or_none()

    def get_all_orders(self, db: Session):
        statement = select(Order)
        result = db.execute(statement)
        return result.scalars().all()

    def update_order_status(self, db: Session, order_id: UUID, status: OrderStatus) -> Order:
        order = self.get_order_by_id(db, order_id)
        if not order:
            raise ValueError("Order not found")
        order.status = status
        db.commit()
        db.refresh(order)
        return order