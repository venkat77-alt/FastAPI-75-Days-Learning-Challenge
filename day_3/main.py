from fastapi import FastAPI,Request
from products import router as product_router
from orders import router as order_router
from middleware import middleware
app = FastAPI(title="Routing and path parameter and query parameter", description="it is day 2 learning modules form my 75 days fastapi learniing challenge. tooday's topics are routing and path parameters and query parameters.")

@app.middleware("http")
async def Application_middleware(request: Request, call_next):
    return await middleware(request, call_next)

app.include_router(product_router, prefix="/products", tags=["products"])

app.include_router(order_router, prefix="/orders", tags=["orders"])

