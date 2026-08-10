from fastapi import FastAPI
from app.api.routes.order_router import router as order_router
from app.db.init_db import init_db

app = FastAPI(
    title="Order Service",
    version="1.0.0"
)

init_db()

@app.get("/")
def root():
    return {
        "message": "Order Service is running!"
    }

app.include_router(order_router)