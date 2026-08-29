from fastapi import FastAPI, HTTPException,Request
from fastapi.middleware import Middleware

from products import router as product_router
from orders import router as order_router
from Middleware.middleware import Http_middleware

from Exception_handler.exception_handler import global_http_exception_handler


app = FastAPI(title="Routing and path parameter and query parameter", description="it is day 2 learning modules form my 75 days fastapi learniing challenge. tooday's topics are routing and path parameters and query parameters.")

@app.middleware("http")
async def Application_middleware(request: Request, call_next):
    return await Http_middleware(request, call_next)

app.exception_handler(global_http_exception_handler)

app.include_router(product_router, prefix="/products", tags=["products"])

app.include_router(order_router, prefix="/orders", tags=["orders"])

