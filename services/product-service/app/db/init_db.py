from app.db.session import engine
from app.models.product import Product
from app.models.base import Base

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")