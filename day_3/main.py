from fastapi import FastAPI, HTTPException,Request
from fastapi.middleware import Middleware

from products import router as product_router
from orders import router as order_router
from Middleware.middleware import Http_middleware

from Exception_handler.exception_handler import global_http_exception_handler,global_general_exception_handler


app = FastAPI(title="Middleware, Global Exception handler", description="it is day 3 learning modules form my 75 days fastapi learniing challenge. tooday's topics are Middleware, Global Exception Handler.")

@app.middleware("http")
async def Application_middleware(request: Request, call_next):
    return await Http_middleware(request, call_next)

app.add_exception_handler(HTTPException,global_http_exception_handler)
app.add_exception_handler(Exception,global_general_exception_handler)


app.include_router(product_router, prefix="/products", tags=["products"])

app.include_router(order_router, prefix="/orders", tags=["orders"])

