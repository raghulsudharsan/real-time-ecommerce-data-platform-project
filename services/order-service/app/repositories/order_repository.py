from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.order import Order
from app.models.order_item import OrderItem

class OrderRepository:
    def create_order(self, db: Session, order: Order) -> Order:
        db.add(order)
        db.flush()
        db.refresh(order)

        return order
    
    def create_order_item(self,db: Session,order_item: OrderItem) -> OrderItem:
        db.add(order_item)
        db.flush()
        db.refresh(order_item)

        return order_item
    
    def get_order_by_id(self,db: Session,order_id: UUID) -> Order | None:
        statement = (
        select(Order)
        .where(Order.id == order_id))

        result = db.execute(statement)

        return result.scalar_one_or_none()