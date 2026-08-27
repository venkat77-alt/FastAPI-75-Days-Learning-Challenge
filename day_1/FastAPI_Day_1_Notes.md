# FastAPI 75-Day Learning Challenge
# Day 1 — Async Python Mechanics & FastAPI Environment Setup

---

## 1. Day 1 Overview

Day 1 is the foundation for understanding asynchronous Python and FastAPI.

### Main Topics

- Synchronous programming
- Asynchronous programming
- `async`
- `await`
- `asyncio`
- Event loop
- Coroutines
- Blocking vs non-blocking I/O
- Async vs multithreading
- Python virtual environment
- FastAPI installation
- Uvicorn
- Creating FastAPI applications
- Async FastAPI endpoints
- Helper async functions
- `asyncio.sleep()`
- `asyncio.gather()`
- E-commerce async practice

---

# 2. Synchronous Programming

Synchronous programming executes tasks one after another.

```python
def task_one():
    print("Task 1 started")
    print("Task 1 completed")


def task_two():
    print("Task 2 started")
    print("Task 2 completed")


task_one()
task_two()
```

Execution:

```text
Task 1 starts
    ↓
Task 1 completes
    ↓
Task 2 starts
    ↓
Task 2 completes
```

The second task waits for the first task to finish.

---

# 3. Asynchronous Programming

Asynchronous programming is useful when programs spend time waiting for I/O operations such as:

- Database requests
- API requests
- Network requests
- External services
- Suitable file I/O

Python provides `asyncio` for asynchronous programming.

```python
import asyncio


async def task_one():
    print("Task 1 started")

    await asyncio.sleep(2)

    print("Task 1 completed")


async def main():
    await task_one()


asyncio.run(main())
```

---

# 4. What Does `async` Mean?

```python
async def task_one():
```

defines an asynchronous function, also called a coroutine function.

Example:

```python
async def db_check():
    ...
```

An asynchronous function can use `await` for asynchronous operations.

---

# 5. What Does `await` Mean?

`await` waits for an asynchronous operation while allowing the event loop to manage other available asynchronous work.

Example:

```python
async def db_check():

    await asyncio.sleep(1)

    return {
        "status": "db connected successfully"
    }
```

Mental model:

```text
async
↓
Function can perform asynchronous work

await
↓
Wait for an async operation
```

---

# 6. What Is `asyncio`?

`asyncio` is Python's library for asynchronous programming.

```python
import asyncio
```

Important tools:

```python
asyncio.sleep()
asyncio.gather()
asyncio.run()
```

---

# 7. What Is an Event Loop?

The event loop manages asynchronous tasks and coroutines.

Conceptually:

```text
                Event Loop
                    |
        +-----------+-----------+
        |                       |
      Task 1                  Task 2
        |                       |
     waiting                  running
        |                       |
        +-----------+-----------+
                    |
              Continue work
```

For example:

```python
await asyncio.sleep(1)
```

allows the current coroutine to wait cooperatively while the event loop can manage other asynchronous work.

---

# 8. Blocking vs Non-Blocking

## Blocking

```text
Start
 ↓
Database request
 ↓
WAIT
 ↓
Database response
 ↓
Continue
```

## Non-blocking I/O

```text
Start
 ↓
Database request
 ↓
Waiting
 ↓
Event loop can handle other async work
 ↓
Database response
 ↓
Continue
```

Async programming is especially useful for suitable I/O-bound workloads.

---

# 9. Async Does Not Automatically Make Everything Faster

This is important:

```text
async ≠ faster for everything
```

For example:

```python
async def calculate():

    for i in range(100000000):
        ...
```

A CPU-heavy loop does not automatically become asynchronous just because the function uses `async def`.

Async is especially useful for suitable I/O-bound work.

---

# 10. Async vs Multithreading

## Async

```text
Event Loop
   ↓
Task A
Task B
Task C
```

## Multithreading

```text
Process
   |
   +── Thread 1
   |
   +── Thread 2
   |
   +── Thread 3
```

Remember:

```text
Async
→ event loop
→ coroutines
→ async/await
→ suitable I/O-bound workloads
```

```text
Multithreading
→ multiple threads
→ useful for certain workloads and blocking operations
```

---

# 11. FastAPI Environment Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install FastAPI and Uvicorn:

```bash
pip install fastapi uvicorn
```

---

# 12. What Is Uvicorn?

Uvicorn is an ASGI server commonly used to run FastAPI applications.

```text
Client
   ↓
HTTP request
   ↓
Uvicorn
   ↓
FastAPI
   ↓
Endpoint
   ↓
Response
```

Run:

```bash
uvicorn main:app --reload
```

Here:

```text
main
↓
main.py

app
↓
FastAPI application object
```

---

# 13. First FastAPI Application

```python
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def home():

    return {
        "message": "Hello World"
    }
```

Run:

```bash
uvicorn main:app --reload
```

Visit:

```text
http://127.0.0.1:8000/
```

Expected response:

```json
{
    "message": "Hello World"
}
```

---

# 14. Understanding the FastAPI Code

```python
from fastapi import FastAPI
```

Imports FastAPI.

```python
app = FastAPI()
```

Creates the FastAPI application.

```python
@app.get("/")
```

Creates a GET route for `/`.

```python
async def home():
```

Creates an asynchronous endpoint function.

```python
return {
    "message": "Hello World"
}
```

Returns the API response.

---

# 15. Your Enterprise System Diagnostic API

Your main Day 1 practical example:

```python
import asyncio
import psutil

from fastapi import FastAPI


app = FastAPI(
    title="Enterprise System Diagnostic API",
    version="1.0.0"
)


async def db_check():

    await asyncio.sleep(1)

    return {
        "status": "db connected successfully"
    }


@app.get("/db_check")
async def db_connection_check():

    return await db_check()


@app.get("/system_matrix")
async def system_matrix():

    ram_usage = psutil.virtual_memory()

    return {
        "db_status": await db_check(),

        "cpu_usage": f"{psutil.cpu_percent(interval=None)}%",

        "total_ram_gb": round(
            ram_usage.total / (1024 ** 3),
            2
        ),

        "used_ram_gb": round(
            ram_usage.used / (1024 ** 3),
            2
        ),

        "available_ram_gb": round(
            ram_usage.available / (1024 ** 3),
            2
        )
    }
```

---

# 16. Understanding `db_check()`

```python
async def db_check():

    await asyncio.sleep(1)

    return {
        "status": "db connected successfully"
    }
```

The function is asynchronous.

```python
async def db_check():
```

simply defines the coroutine function.

Then:

```python
await asyncio.sleep(1)
```

simulates one second of asynchronous waiting.

Important:

This does **not** actually connect to PostgreSQL. It is a simulation of database/network waiting.

---

# 17. Why `asyncio.sleep()`?

We used:

```python
await asyncio.sleep(1)
```

because we did not yet have a real database.

It gives us a simple way to practice asynchronous waiting.

Compare:

```python
time.sleep(1)
```

with:

```python
await asyncio.sleep(1)
```

`time.sleep()` is blocking, while `asyncio.sleep()` cooperates with the asynchronous event loop.

---

# 18. Your `/db_check` Endpoint

```python
@app.get("/db_check")
async def db_connection_check():

    return await db_check()
```

Request:

```text
GET /db_check
```

Flow:

```text
HTTP request
    ↓
db_connection_check()
    ↓
await db_check()
    ↓
asyncio.sleep(1)
    ↓
result
    ↓
HTTP response
```

---

# 19. Why Use a Helper Function?

Instead of placing all logic directly inside the endpoint:

```python
@app.get("/db_check")
async def db_connection_check():

    await asyncio.sleep(1)

    return {
        "status": "db connected successfully"
    }
```

you separated the operation:

```python
async def db_check():
    ...
```

and called it from the route:

```python
return await db_check()
```

This creates a basic separation:

```text
Route handling
      ↓
Helper / business logic
```

---

# 20. Route Function vs Helper Function

The route:

```python
@app.get("/db_check")
async def db_connection_check():
    return await db_check()
```

is a FastAPI route.

The helper:

```python
async def db_check():
    ...
```

is a normal Python asynchronous helper function.

Conceptually:

```text
HTTP request
     ↓
FastAPI route
     ↓
Helper / business function
     ↓
Result
     ↓
HTTP response
```

---

# 21. Understanding `/system_matrix`

```python
@app.get("/system_matrix")
async def system_matrix():

    ram_usage = psutil.virtual_memory()

    return {
        "db_status": await db_check(),

        "cpu_usage": f"{psutil.cpu_percent(interval=None)}%",

        "total_ram_gb": round(
            ram_usage.total / (1024 ** 3),
            2
        ),

        "used_ram_gb": round(
            ram_usage.used / (1024 ** 3),
            2
        ),

        "available_ram_gb": round(
            ram_usage.available / (1024 ** 3),
            2
        )
    }
```

This endpoint combines:

```text
Database simulation
+
CPU information
+
RAM information
```

---

# 22. Understanding `psutil`

You imported:

```python
import psutil
```

Memory information:

```python
psutil.virtual_memory()
```

CPU information:

```python
psutil.cpu_percent(interval=None)
```

---

# 23. RAM Calculation

```python
ram_usage = psutil.virtual_memory()
```

RAM values are returned in bytes.

Convert bytes to GB:

```python
ram_usage.total / (1024 ** 3)
```

Round to two decimal places:

```python
round(
    ram_usage.total / (1024 ** 3),
    2
)
```

The same approach is used for:

```python
ram_usage.used
ram_usage.available
```

---

# 24. Important Async Observation From Your Code

Your route is:

```python
async def system_matrix():
```

But not every operation inside it is asynchronous.

For example:

```python
ram_usage = psutil.virtual_memory()
```

is a synchronous `psutil` call.

Likewise:

```python
psutil.cpu_percent(interval=None)
```

is not an async function.

The async operation in the route is:

```python
await db_check()
```

Important lesson:

```text
async def
≠
everything inside automatically becomes async
```

---

# 25. `asyncio.gather()`

You also practiced:

```python
results = await asyncio.gather(
    order_details(order_id),
    payment_details(order_id)
)
```

`gather()` is useful when multiple independent asynchronous operations can be handled concurrently.

---

# 26. Why `gather()` Is Useful

Suppose an order workflow needs:

```text
Order details
+
Payment details
```

and neither operation depends on the other.

Sequential concept:

```text
order_details()
      ↓
wait
      ↓
payment_details()
      ↓
wait
```

With `gather()`:

```python
results = await asyncio.gather(
    order_details(order_id),
    payment_details(order_id)
)
```

Conceptually:

```text
             ┌── order_details()
             │
Start ───────┤
             │
             └── payment_details()

        ↓

    both complete

        ↓

     results
```

---

# 27. E-Commerce Async Practice

Your e-commerce practice used the idea of getting order and payment information asynchronously.

```python
import asyncio


async def order_details(order_id):

    await asyncio.sleep(2)

    return {
        "order_id": order_id,
        "item": "mobile",
        "quantity": 2
    }


async def payment_details(order_id):

    await asyncio.sleep(2)

    return {
        "order_id": order_id,
        "payment_status": "paid"
    }


async def get_order_information(order_id):

    results = await asyncio.gather(
        order_details(order_id),
        payment_details(order_id)
    )

    return results
```

---

# 28. What Happens in `gather()`?

```python
results = await asyncio.gather(
    order_details(order_id),
    payment_details(order_id)
)
```

Both independent coroutines are scheduled for concurrent execution by the event loop.

After both complete:

```python
results
```

contains their results.

Conceptually:

```python
[
    {
        "order_id": 1,
        "item": "mobile",
        "quantity": 2
    },
    {
        "order_id": 1,
        "payment_status": "paid"
    }
]
```

---

# 29. When Should You Use `gather()`?

Use it when:

1. You have multiple async operations.
2. They are independent.
3. One does not need the result of another before starting.

Good example:

```text
Get order details
+
Get payment information
```

Potential examples:

```text
Get product details
+
Get recommendations
+
Get inventory
```

Do not use it simply because two operations exist.

If operation B depends on operation A:

```text
Create user
    ↓
Get newly created user ID
    ↓
Create user profile
```

there is a dependency.

---

# 30. Async Function vs Async Operation

Writing:

```python
async def get_products():
```

does not automatically make every operation inside asynchronous.

Example:

```python
async def get_products():

    products = some_sync_function()

    return products
```

`some_sync_function()` is still synchronous.

Therefore:

```text
async def
≠
everything inside automatically async
```

Instead:

```text
async def
+
await suitable async operations
```

creates an asynchronous workflow.

---

# 31. Common Day 1 Mistakes

## Mistake 1 — Blocking sleep

Avoid:

```python
time.sleep(1)
```

when specifically practicing asynchronous waiting.

Use:

```python
await asyncio.sleep(1)
```

for the simulation.

## Mistake 2 — Thinking async makes CPU-heavy code faster

It does not.

## Mistake 3 — Thinking every function inside an async endpoint is asynchronous

It isn't.

## Mistake 4 — Forgetting `await`

Incorrect:

```python
result = db_check()
```

Correct:

```python
result = await db_check()
```

when `db_check()` is an async coroutine that needs to be awaited.

## Mistake 5 — Reusing route functions as business logic

Prefer:

```python
async def db_check():
    ...
```

and:

```python
@app.get("/db_check")
async def db_connection_check():
    return await db_check()
```

---

# 32. Day 1 Practical Architecture

The main pattern introduced:

```text
FastAPI Route
     ↓
Helper / Business Logic
     ↓
Async I/O
```

Example:

```python
async def db_check():
    await asyncio.sleep(1)
    return {"status": "connected"}


@app.get("/db_check")
async def db_connection_check():
    return await db_check()
```

---

# 33. Day 1 Quick Reference

### Synchronous function

```python
def function():
    ...
```

### Asynchronous function

```python
async def function():
    ...
```

### Await

```python
result = await async_function()
```

### Async sleep

```python
await asyncio.sleep(1)
```

### Run an async Python program

```python
asyncio.run(main())
```

### Multiple independent async operations

```python
results = await asyncio.gather(
    task_one(),
    task_two()
)
```

### FastAPI application

```python
from fastapi import FastAPI

app = FastAPI()
```

### FastAPI async route

```python
@app.get("/")
async def home():

    return {
        "message": "Hello World"
    }
```

### Run FastAPI

```bash
uvicorn main:app --reload
```

---

# 34. Day 1 Complete Mental Model

```text
Python
   ↓
asyncio
   ↓
Event Loop
   ↓
Coroutines
   ↓
async / await
   ↓
Non-blocking I/O
   ↓
FastAPI async endpoints
   ↓
Helper async functions
   ↓
asyncio.gather()
   ↓
Real API I/O workflows
```

---

# 35. What You Practiced

## Practice 1 — Async Concepts

```python
async def
await
asyncio.sleep()
```

## Practice 2 — FastAPI Environment

You created a FastAPI application and learned how to run it with Uvicorn.

## Practice 3 — Diagnostic API

You created:

```text
GET /db_check
GET /system_matrix
```

The API simulated database I/O and collected CPU/RAM information.

## Practice 4 — Helper Function

You separated:

```python
db_check()
```

from:

```python
db_connection_check()
```

## Practice 5 — E-Commerce Async Workflow

You practiced:

```python
order_details(order_id)
payment_details(order_id)
```

and:

```python
await asyncio.gather(
    order_details(order_id),
    payment_details(order_id)
)
```

---

# 36. Day 1 Checklist

## Async Python

- [x] Synchronous programming
- [x] Asynchronous programming
- [x] `async`
- [x] `await`
- [x] `asyncio`
- [x] Event loop
- [x] Coroutines
- [x] Blocking vs non-blocking
- [x] Non-blocking I/O
- [x] Async vs multithreading
- [x] `asyncio.sleep()`
- [x] `asyncio.gather()`

## FastAPI Setup

- [x] Virtual environment
- [x] FastAPI installation
- [x] Uvicorn
- [x] FastAPI application
- [x] GET endpoint
- [x] Async endpoint
- [x] Running the application

## Practical FastAPI

- [x] Helper async function
- [x] `await` helper function
- [x] Database I/O simulation
- [x] System diagnostic endpoint
- [x] CPU information
- [x] RAM information
- [x] E-commerce async practice
- [x] `asyncio.gather()` practice

---

# 37. Final Day 1 Summary

```text
async def
→ defines an asynchronous function

await
→ waits for an async operation while cooperating with the event loop

asyncio
→ Python's asynchronous programming library

Event loop
→ manages asynchronous tasks/coroutines

asyncio.sleep()
→ asynchronous waiting/simulation

asyncio.gather()
→ handles multiple independent async operations concurrently

FastAPI
→ web framework used to build APIs

Uvicorn
→ ASGI server used to run the FastAPI application
```

Most important practical pattern:

```python
async def helper():
    await some_async_operation()
    return result


@app.get("/example")
async def example():
    return await helper()
```

For multiple independent async operations:

```python
results = await asyncio.gather(
    task_one(),
    task_two()
)
```

---

# 38. Day 1 → Day 2 Connection

Day 1:

```text
Async Python + FastAPI Core
          ↓
Async endpoints
```

Day 2:

```text
FastAPI
     ↓
Routing
     ↓
Route Controllers
     ↓
Path Parameters
     ↓
Query Parameters
     ↓
Path() / Query() Validation
```

Progression:

```text
DAY 1
Async Python + FastAPI Core
          ↓
DAY 2
Routing + Parameters
          ↓
DAY 3
Middleware + Global Exception Handling
          ↓
DAY 4
Pydantic v2
```

---

# END OF DAY 1 NOTES
