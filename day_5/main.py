from fastapi import FastAPI, HTTPException,Request
from login import router as login_router


from routers.products import router as product_router
from routers.orders import router as order_router
from Middleware.middleware import Http_middleware

from Exception_handler.exception_handler import global_http_exception_handler,global_general_exception_handler


app = FastAPI(title="Advanced pydantic v2", description="it is day 5 learning modules form my 75 days fastapi learniing challenge. tooday's topic is advnaced pydantic v2.")

@app.middleware("http")
async def Application_middleware(request: Request, call_next):
    return await Http_middleware(request, call_next)

app.add_exception_handler(HTTPException,global_http_exception_handler)
app.add_exception_handler(Exception,global_general_exception_handler)


app.include_router(product_router, prefix="/products", tags=["products"])

app.include_router(order_router, prefix="/orders", tags=["orders"])
app.include_router(login_router, prefix="/login", tags=["login"])

