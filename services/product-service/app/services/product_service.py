from itertools import product
import json
from app.db.redis import redis_client
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate
from sqlalchemy.orm import Session 
from uuid import UUID
from fastapi import HTTPException
class ProductService: 

    def __init__(self,repository: ProductRepository):
        self.repository = repository

    def create_product(self, db: Session, request: ProductCreate):
        product = self.repository.create_product(db=db, product=request)
        return product   

    '''def get_product_by_id(self, db: Session, product_id: UUID):
        product = self.repository.get_product_by_id(db=db, product_id=product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product '''

    def get_product_by_id(self, db: Session, product_id: UUID):

        cache_key = f"product:{product_id}"

        # 1. Check Redis
        cached_product = redis_client.get(cache_key)

        if cached_product:
            print("🔥 Redis CACHE HIT")
            return json.loads(cached_product)

        print("❌ Redis CACHE MISS")

        # 2. Cache miss → PostgreSQL
        product = self.repository.get_product_by_id(
        db=db,
        product_id=product_id
    )

        if product is None:
            raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

        # 3. Convert product to JSON-friendly data
        product_data = {
        "id": str(product.id),
        "name": product.name,
        "price": str(product.price),
        "brand": product.brand,
        "storage": product.storage,
        "color": product.color,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat(),
    }

        # 4. Store in Redis for 5 minutes
        redis_client.set(
        cache_key,
        json.dumps(product_data),
        ex=300
    )

        return product

    def get_all_products(self, db: Session):
        products = self.repository.get_all_products(db=db)
        return products

    def update_product(self, db:Session, product_id: UUID, request: ProductUpdate):
        product = self.repository.update_product(db=db, product_id=product_id, product=request)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def get_products_by_ids(self, db: Session, product_ids: list[UUID]):
        products = self.repository.get_products_by_ids(db=db, product_ids=product_ids)
        requested_ids = set(product_ids)
        found_ids = {product.id for product in products}
        missing_ids = requested_ids - found_ids
        if missing_ids:
            raise HTTPException(
                status_code=404,
                detail=f"Products with IDs {', '.join(str(id) for id in missing_ids)} not found"
            )
        return products