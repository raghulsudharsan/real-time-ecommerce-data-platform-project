
from fastapi import FastAPI, HTTPException, Request
import httpx

app = FastAPI(
    title="E-Commerce API Gateway",
)

#PRODUCT_SERVICE_URL = "http://localhost:8001"
#ORDER_SERVICE_URL = "http://localhost:8000"
PRODUCT_SERVICE_URL = "http://product-service:8000"
ORDER_SERVICE_URL = "http://order-service:8000"

async def forward_request(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    **kwargs,
):
    try:
        response = await client.request(
            method=method,
            url=url,
            **kwargs,
        )

        response.raise_for_status()

        return response

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Downstream service unavailable",
        )

@app.get("/health")
def health():
    return {
        "service": "api-gateway",
        "status": "healthy",
    }


@app.get("/api/products")
async def get_products():
    async with httpx.AsyncClient() as client:
        response = await forward_request(
        client=client,
        method="GET",
        url=f"{PRODUCT_SERVICE_URL}/products/",
)
    return response.json()

@app.get("/api/orders")
async def get_orders():

    async with httpx.AsyncClient() as client:

        response = await forward_request(
            client=client,
            method="GET",
            url=f"{ORDER_SERVICE_URL}/orders/",
        )

        return response.json()

@app.post("/api/orders")
async def create_order(
    request: Request,
):

    body = await request.json()

    headers = {
        "Authorization": request.headers.get("Authorization"),
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:

        response = await forward_request(
            client=client,
            method="POST",
            url=f"{ORDER_SERVICE_URL}/orders/",
            headers=headers,
            json=body,
        )

        return response.json()

@app.post("/api/auth/login")
async def login(request: Request):

    body = await request.body()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    async with httpx.AsyncClient() as client:

        response = await forward_request(
            client=client,
            method="POST",
            url=f"{ORDER_SERVICE_URL}/auth/login",
            headers=headers,
            content=body,
        )

        return response.json()
    