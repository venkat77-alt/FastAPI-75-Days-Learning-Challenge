import asyncio
import psutil
from fastapi import FastAPI

app = FastAPI(title="something", description="something")


async def order_details(order_id: int):
    await asyncio.sleep(1)
    return {
        "order_id": order_id,
        "order_details": {
            "item": "iphone",
            "price": 1000,
            "quantity": 1,
        },
    }


async def payment_details(order_id: int):
    await asyncio.sleep(1)
    return {
        "order_id": order_id,
        "payment_details": {
            "payment_status": "success",
            "payment_method": "UPI",
        },
    }


@app.get("/order_details/{order_id}")
async def get_order_details(order_id: int):
    await asyncio.sleep(1)
    ram_usage = psutil.virtual_memory()


    results = await asyncio.gather(order_details(order_id), payment_details(order_id))
    return {
        "order_details": results[0],
        "payment_details": results[1],
        "total_ram_gb": round(ram_usage.total / (1024 ** 3), 2),
        "used_ram_gb": round(ram_usage.used / (1024 ** 3), 2),
        "available_ram_gb": round(ram_usage.available / (1024 ** 3), 2),
        "ram_percentage": f"{ram_usage.percent}%",
        "cpu_usage": f"{psutil.cpu_percent(interval=None)}%"

    }