from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate , ProductBulkRequest
from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.db.session import get_db
from uuid import UUID
router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse)
def create_product(request: ProductCreate, db: Session = Depends(get_db)):
    repository = ProductRepository()
    service = ProductService(repository=repository)
    product = service.create_product(db=db, request=request)
    return product

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: UUID, db: Session = Depends(get_db)):
    repository = ProductRepository()
    service = ProductService(repository=repository)
    product = service.get_product_by_id(db=db, product_id=product_id)
    return product

@router.get("/", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    repository = ProductRepository()
    service = ProductService(repository=repository)
    products = service.get_all_products(db=db)
    return products

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: UUID, request: ProductUpdate, db: Session = Depends(get_db)):
    repository = ProductRepository()
    service = ProductService(repository=repository)
    product = service.update_product(db=db, product_id=product_id, request=request)
    return product

@router.post("/bulk", response_model=list[ProductResponse])
def get_products_by_ids(request: ProductBulkRequest, db: Session = Depends(get_db)):
    repository = ProductRepository()
    service = ProductService(repository=repository)
    products = service.get_products_by_ids(db=db, product_ids=request.product_ids)
    return products