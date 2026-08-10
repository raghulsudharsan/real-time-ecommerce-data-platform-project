from decimal import Decimal
from uuid import uuid4

from app.db.database import SessionLocal
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem

db = SessionLocal()

try:
    print("Step 1: Creating Order object")

    order = Order(
        customer_id=uuid4(),
        status=OrderStatus.PENDING,
        total_amount=Decimal("999.99"),
    )

    print("Step 2: Adding Order to session")

    db.add(order)

    print("Step 3: Flushing Order")

    db.flush()

    print(f"Order ID: {order.id}")

    print("Step 4: Creating Order Items")

    item1 = OrderItem(
        order_id=order.id,
        product_id=uuid4(),
        quantity=2,
    )

    item2 = OrderItem(
        order_id=order.id,
        product_id=uuid4(),
        quantity=1,
    )

    print("Step 5: Adding Order Items")

    db.add_all([item1, item2])

    print("Step 6: Committing Transaction")

    db.commit()

    print("✅ Order created successfully!")

except Exception as e:
    print(f"❌ Error: {e}")

    db.rollback()

    raise

finally:
    print("Closing database session...")
    db.close()