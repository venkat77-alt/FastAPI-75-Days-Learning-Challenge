
---

# 2️⃣ Day 1 `README.md`

Inside:

`day_01/README.md`

```markdown
# Day 1 — Async Python & FastAPI Environment Setup 🚀

## Overview

Day 1 of my FastAPI learning challenge focused on building a foundation in asynchronous Python and setting up a working FastAPI development environment.

The main goal was not just to understand the syntax of `async` and `await`, but to start understanding how asynchronous operations can be used when building backend APIs.

---

## 📚 Topics Covered

### Python Async Fundamentals

- Synchronous vs asynchronous execution
- `def` vs `async def`
- `await`
- `asyncio`
- Understanding the event loop
- Non-blocking I/O concepts
- Practicing multiple asynchronous operations

### FastAPI Environment Setup

- Creating the project
- Creating a Python virtual environment
- Activating the virtual environment
- Installing the required packages
- Setting up FastAPI
- Running the application using Uvicorn
- Creating and testing an API endpoint

---

## 💻 Practical Implementation

For the practical implementation, I created asynchronous functions to simulate different operations such as:

- Retrieving order details
- Retrieving payment details

I then used asynchronous execution to handle these operations together.

The implementation also included a FastAPI endpoint that triggered the asynchronous workflow.

For additional practice, I used `psutil` to retrieve system information such as RAM and CPU usage.

---

## 🔍 API Testing

After starting the FastAPI application, I verified the endpoint through Swagger UI.

The testing process helped me understand the complete flow:

```text
Client Request
      ↓
FastAPI Endpoint
      ↓
Async Functions
      ↓
Async Execution
      ↓
Response
