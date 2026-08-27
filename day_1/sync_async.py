import asyncio
import psutil
from fastapi import FastAPI

app = FastAPI(
    title="Enterprise System Diagnostic API",
    version="1.0.0"
)

# 1. Helper function: Async I/O simulation with delay
async def db_check():
    # Simulates 1-second async network wait with PostgreSQL
    await asyncio.sleep(1)
    return {"status": "db connected successfully"}


@app.get("/db_check")
async def db_connection_check():
    # Calls the helper business logic function
    return await db_check()


@app.get("/system_matrix")
async def system_matrix():
    # 2. Fetch live RAM usage inside the route handler per request
    ram_usage = psutil.virtual_memory()

    return {
        # Call helper coroutine directly instead of calling the endpoint route function
        "db_status": await db_check(),
        "cpu_usage": f"{psutil.cpu_percent(interval=None)}%",
        "total_ram_gb": round(ram_usage.total / (1024 ** 3), 2),
        "used_ram_gb": round(ram_usage.used / (1024 ** 3), 2),
        "available_ram_gb": round(ram_usage.available / (1024 ** 3), 2),
    }