from fastapi import FastAPI
from app.api.routes.order_router import router as order_router

app = FastAPI(
    title="Real-Time E-Commerce Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Order Service is running!"
    }

app.include_router(order_router)