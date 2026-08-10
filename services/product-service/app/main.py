from fastapi import FastAPI
from app.api.routes.product_router import router 

app = FastAPI(title="Product Service", version="1.0.0")
app.include_router(router)