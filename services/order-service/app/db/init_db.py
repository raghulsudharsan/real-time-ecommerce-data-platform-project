from app.db.database import engine
from app.models.base import Base
from app.models.order import Order
from app.models.order_item import OrderItem

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")