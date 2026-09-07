# 🚀 FastAPI 75-Day Learning Challenge — Day 3

## 📌 Day 3: Middleware & Global Exception Handling

Today I focused on two important concepts used in production FastAPI applications:

- **HTTP Middleware**
- **Global Exception Handling**

The goal was to understand how requests and responses can be processed centrally and how API errors can be handled consistently across the application.

---

# 🎯 What I Learned

## 1. HTTP Middleware

Middleware is code that runs during the request/response lifecycle.

It allows common operations to be handled centrally instead of repeating the same logic inside every endpoint.

### Basic Flow

```text
Client
   ↓
Request
   ↓
Middleware
   ↓
FastAPI Router
   ↓
Endpoint
   ↓
Response
   ↓
Middleware
   ↓
Client
```

The middleware can therefore perform operations:

- Before the endpoint executes
- After the endpoint executes
- Around the complete request/response lifecycle

---

# 🔧 2. Creating HTTP Middleware

FastAPI provides:

```python
@app.middleware("http")
```

Example:

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def application_middleware(request: Request, call_next):
    print("Request received")

    response = await call_next(request)

    print("Response generated")

    return response
```

The important parts are:

```python
request
```

and:

```python
call_next
```

`request` contains information about the incoming HTTP request.

`call_next` passes the request to the next middleware/endpoint and returns the generated response.

---

# 🆔 3. Generating a Request ID

A unique request ID can be generated for every incoming request.

This is useful for identifying individual requests in logs and debugging.

```python
import uuid

request_id = str(uuid.uuid4())
```

Example:

```text
Request ID:
550e8400-e29b-41d4-a716-446655440000
```

Every request can therefore have its own unique identifier.

---

# 🗃️ 4. Request State

FastAPI provides:

```python
request.state
```

to store information that can be accessed later during the same request.

For example:

```python
request.state.request_id = request_id
```

The request ID can then be accessed from another part of the application:

```python
request.state.request_id
```

This becomes especially useful when an exception handler needs to return the request ID.

---

# ⏱️ 5. Measuring Request Processing Time

The middleware can measure how long a request takes.

Python's:

```python
time.perf_counter()
```

can be used for high-resolution timing.

Example:

```python
import time

start_time = time.perf_counter()

response = await call_next(request)

end_time = time.perf_counter()

process_time = end_time - start_time
```

This gives the approximate processing time for the request.

---

# 📋 6. Reading Request Information

The middleware can inspect different request properties.

### HTTP Method

```python
request.method
```

Example:

```text
GET
POST
PUT
DELETE
```

### Request Path

```python
request.url.path
```

Example:

```text
/products/
```

### User-Agent

```python
request.headers.get("user-agent")
```

This can provide information about the client making the request.

### Request Headers

```python
request.headers
```

---

# 📤 7. Adding Response Headers

Middleware can also modify the response before sending it back to the client.

For example:

```python
response.headers["X-Request-ID"] = request_id
response.headers["X-Process-Time"] = str(process_time)
```

The client can then receive headers such as:

```text
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
X-Process-Time: 0.00231
```

These headers can be useful for debugging and monitoring.

---

# 🧩 Complete Middleware Implementation

The middleware created during Day 3:

```python
from fastapi import Request
import time
import uuid


async def Http_middleware(request: Request, call_next):

    request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    start_time = time.perf_counter()

    print("========Request received========")
    print("Request ID:", request_id)
    print("Method:", request.method)
    print("Path:", request.url.path)
    print("Headers:", request.headers.get("user-agent"))
    print("Request State:", request.state)

    response = await call_next(request)

    end_time = time.perf_counter()

    process_time = end_time - start_time

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)

    print("========Response generated========")
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Process Time:", process_time)
    print("Response Background:", response.background)

    return response
```

---

# 🏗️ 8. Separating Middleware Logic

Instead of putting all middleware logic directly inside `main.py`, the middleware was separated into its own module.

### Structure

```text
day_3/
│
├── main.py
│
├── Middleware/
│   └── middleware.py
│
├── Exception_handler/
│   └── exception_handler.py
│
├── products.py
└── orders.py
```

The middleware is then imported into `main.py`.

```python
from Middleware.middleware import Http_middleware
```

And registered:

```python
@app.middleware("http")
async def Application_middleware(request: Request, call_next):
    return await Http_middleware(request, call_next)
```

This keeps `main.py` cleaner and separates responsibilities.

---

# ⚠️ 9. Global Exception Handling

APIs can encounter different types of errors.

For example:

- Invalid resource ID
- Missing resource
- Invalid request
- Unexpected server error
- Programming errors

Instead of handling every error separately inside every endpoint, FastAPI allows global exception handlers.

This creates a consistent error response structure.

---

# 🚨 10. Global HTTP Exception Handler

FastAPI provides `HTTPException` for expected HTTP errors.

Example:

```python
from fastapi import HTTPException

raise HTTPException(
    status_code=404,
    detail="Product not found"
)
```

A global handler can catch these errors.

Example:

```python
async def global_http_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "Status": "error",
            "Code": "HTTP Error",
            "Message": exc.detail,
            "Details": None,
            "Request_id": request.state.request_id,
            "Path": request.url.path,
            "Method": request.method
        }
    )
```

This creates a standardized error response.

---

# 💥 11. Global General Exception Handler

Unexpected exceptions can also be handled globally.

Example:

```python
async def global_general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "Status": "error",
            "Code": "INTERNAL SERVER ERROR",
            "Message": "There is something went wrong at server side.",
            "Details": None,
            "Request_id": request.state.request_id,
            "Path": request.url.path,
            "Method": request.method
        }
    )
```

This prevents unexpected errors from producing inconsistent API responses.

---

# 🔌 12. Registering Global Exception Handlers

The handlers are registered in `main.py` using:

```python
app.add_exception_handler(
    HTTPException,
    global_http_exception_handler
)

app.add_exception_handler(
    Exception,
    global_general_exception_handler
)
```

### Important

The correct method for registering an exception handler is:

```python
app.add_exception_handler(...)
```

rather than passing multiple arguments to:

```python
app.exception_handler(...)
```

---

# 🔗 13. Middleware + Exception Handler

One of the important concepts learned today was how these two features work together.

The middleware generates a request ID:

```python
request.state.request_id = request_id
```

If an exception occurs later, the global exception handler can access the same ID:

```python
request.state.request_id
```

Therefore the error response can contain the request ID.

### Complete Flow

```text
Client
   │
   ↓
Middleware
   │
   ├── Generate Request ID
   ├── Store Request ID
   ├── Record Start Time
   │
   ↓
Router / Endpoint
   │
   ├── Success ──────────────┐
   │                         │
   └── Exception             │
          ↓                  │
   Global Exception Handler  │
          │                  │
          ↓                  │
   Standard Error Response   │
          │                  │
          └──────────┬───────┘
                     ↓
                 Middleware
                     │
                     ├── Processing Time
                     ├── Response Headers
                     │
                     ↓
                   Client
```

---

# 🧪 14. Testing Exception Handling

A test endpoint was used to intentionally generate an unexpected error.

Example:

```python
@router.get("/test-error/{num}")
async def test_error(num: int):

    result = 10 / num

    return {
        "result": result
    }
```

Calling:

```text
/test-error/0
```

causes a division-by-zero exception.

Instead of exposing the raw Python exception, the global exception handler returns the standardized error response.

---

# 🐛 15. Debugging Problems During Day 3

During implementation, several issues were encountered and fixed.

### `perf_counter()` Typo

Incorrect:

```python
time.pref_counter()
```

Correct:

```python
time.perf_counter()
```

---

### Incorrect Exception Handler Registration

Incorrect approach:

```python
app.exception_handler(HTTPException, handler)
```

Correct:

```python
app.add_exception_handler(
    HTTPException,
    handler
)
```

---

### Incorrect HTTPException Attribute

Incorrect:

```python
exc.details
```

Correct:

```python
exc.detail
```

`HTTPException` provides the error detail through `exc.detail`.

---

### Incorrect Request ID Access

Incorrect:

```python
request.request_id
```

Correct:

```python
request.state.request_id
```

The request ID was stored inside `request.state`.

---

# 🧠 Key Concepts Learned

### Middleware

```text
Common processing around requests and responses
```

### Request State

```text
Temporary data associated with the current request
```

### Request ID

```text
Unique identifier used to trace a request
```

### `perf_counter()`

```text
Used to measure request processing time
```

### Exception Handler

```text
Centralized handling of API errors
```

### `JSONResponse`

```text
Used to return custom JSON error responses
```

---

# 📊 Day 3 Architecture

```text
                    FastAPI Application
                           │
                           ↓
                    HTTP Middleware
                           │
             ┌─────────────┴─────────────┐
             │                           │
       Request ID                   Start Timer
             │
             ↓
        Request State
             │
             ↓
          Router
             │
             ↓
          Endpoint
             │
       ┌─────┴─────┐
       │           │
    Success      Error
       │           │
       │           ↓
       │    Global Exception
       │       Handler
       │           │
       └─────┬─────┘
             ↓
          Response
             │
             ↓
       Middleware
             │
       ┌─────┴─────┐
       │           │
  Process Time  Response
                Headers
       │           │
       └─────┬─────┘
             ↓
           Client
```

---

# 🏆 Day 3 Completed

Day 3 provided a practical understanding of how FastAPI can handle cross-cutting concerns such as:

- Request logging
- Request identification
- Processing-time measurement
- Request state
- Response headers
- Centralized HTTP errors
- Unexpected server errors

These concepts form an important foundation for building more structured and maintainable FastAPI applications.

---

## 🚀 Next: Day 4

**Pydantic v2 Fundamentals**

Topics:

- `BaseModel`
- Request body validation
- Automatic type conversion
- Strict mode
- Default values
- Field descriptions
- Nested schemas
- Pydantic integration with FastAPI endpoints

---

### 📚 Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Swagger / OpenAPI