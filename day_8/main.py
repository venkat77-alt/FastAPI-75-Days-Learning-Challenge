from fastapi import FastAPI, HTTPException,Request
from user import router as login_router
from config.settings import settings

from routers.profile import router as profile_router
from routers.products import router as product_router
from routers.orders import router as order_router
from Middleware.middleware import Http_middleware

from Exception_handler.exception_handler import global_http_exception_handler,global_general_exception_handler


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.app_debug
)

@app.middleware("http")
async def Application_middleware(request: Request, call_next):
    return await Http_middleware(request, call_next)

app.add_exception_handler(HTTPException,global_http_exception_handler)
app.add_exception_handler(Exception,global_general_exception_handler)


app.include_router(product_router, prefix="/products", tags=["products"])

app.include_router(order_router, prefix="/orders", tags=["orders"])
app.include_router(login_router, prefix="", tags=["login"])
app.include_router(profile_router,prefix="/current_user_profile",tags=["current_user_profile"])


