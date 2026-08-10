import httpx
from uuid import UUID


class ProductClient:

    def get_products(self, product_ids : list[UUID]):
        response = httpx.post("http://product-service:8000/products/bulk", json={"product_ids": [str(id) for id in product_ids]})
        return response.json()
