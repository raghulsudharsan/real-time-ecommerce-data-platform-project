from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.services.order_service import OrderService
from app.schemas.order import OrderResponse

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/")
def create_order(
    request: OrderCreate,
    db: Session = Depends(get_db),
):
    repository = OrderRepository()
    service = OrderService(repository)

    return service.create_order(
        db=db,
        request=request,
    )

@router.get("/{order_id}")
def get_order_by_id(
    order_id: UUID,
    db: Session = Depends(get_db),
):
    repository = OrderRepository()
    service = OrderService(repository)

    return service.get_order_by_id(
        db=db,
        order_id=order_id,
    )

@router.get("/", response_model=list[OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    repository = OrderRepository()
    service = OrderService(repository=repository)
    return service.get_all_orders(db=db)

@router.patch("/{order_id}/status")
def update_order_status(
    order_id: UUID,
    request: OrderStatusUpdate,
    db: Session = Depends(get_db),
):
    repository = OrderRepository()
    service = OrderService(repository=repository)
    return service.update_order_status(
        db=db,
        order_id=order_id,
        request=request,
    )