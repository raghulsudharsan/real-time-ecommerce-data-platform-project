from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate
from app.services.order_service import OrderService

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