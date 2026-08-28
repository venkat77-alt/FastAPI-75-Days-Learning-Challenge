from fastapi import FastAPI,Request
import time
from products import router as product_router
from orders import router as order_router

app = FastAPI(title="Routing and path parameter and query parameter", description="it is day 2 learning modules form my 75 days fastapi learniing challenge. tooday's topics are routing and path parameters and query parameters.")

@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = time.perf_counter()

    print("========Request received========")
    print("Method:", request.method)
    print("path:", request.url.path)
    print("headers:" , request.headers.get("user-agent"))

    response = await call_next(request)

    print("========Response generated========")
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    end_time = time.perf_counter()
    process_time = end_time - start_time
    print("Process Time:", process_time)
    return response

app.include_router(product_router, prefix="/products", tags=["products"])

app.include_router(order_router, prefix="/orders", tags=["orders"])

