from uuid import UUID

from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate , ProductUpdate
class ProductRepository:
    def create_product(self,db: Session, product: ProductCreate):
        db_product = Product(**product.model_dump())
        db.add(db_product)

        db.commit()

        db.refresh(db_product)

        return db_product

    def get_product_by_id(self,db:Session, product_id:UUID):
        return db.query(Product).filter(Product.id == product_id).first()
    
    def get_all_products(self, db: Session):
        return db.query(Product).all()

    def update_product(self,db: Session, product_id:UUID, product: ProductUpdate):
        db_product = self.get_product_by_id(
    db=db,
    product_id=product_id)
        #db_product = db.query(Product).filter(Product.id == product_id).first()
        if db_product is None:
            return None
        for key, value in product.model_dump(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product

    def get_products_by_ids(self,db: Session,product_ids: list[UUID]):
        return (db.query(Product).filter(Product.id.in_(product_ids)).all())