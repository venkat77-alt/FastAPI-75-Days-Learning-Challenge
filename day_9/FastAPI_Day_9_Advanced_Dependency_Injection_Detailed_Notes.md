# FastAPI Day 9 — Advanced Dependency Injection, Sub-dependencies, Lifecycle Cleanup, and Testing

> **75-Day FastAPI Learning Challenge**  
> **Project:** Your existing e-commerce API (`products`, `orders`, and `profile`)  
> **Day 9 focus:** Dependency chaining, `yield`, `try/finally`, role checks, dependency overrides, and pytest.

**Scope note:** These notes document your actual Day 9 implementation. `get_current_user()` currently returns a mock user dictionary. It does not yet validate JWTs, authenticate a bearer token, or load a user from a database. Those are later roadmap topics.

## Contents

1. Learning goals
2. Day 8 recap
3. Sub-dependencies
4. Dependency chain in your project
5. `get_current_user()` and its code
6. `yield` versus `return`
7. `try/finally` and cleanup
8. The `is_admin()` dependency
9. The `/profile/is_admin` route
10. Current-user profile route
11. Account-status service
12. Dependency overrides
13. Your pytest test
14. Request lifecycle walkthrough
15. Running the test
16. Architecture overview
17. Day 8 versus Day 9
18. Common mistakes and distinctions
19. What this implementation does and does not prove
20. Revision questions
21. Completion checklist
22. Final mental model

---

# 1. Day 9 Learning Goals

By the end of Day 9, you should be able to explain and identify in your own project:

- What a sub-dependency is.
- How one dependency can depend on another.
- How FastAPI resolves a dependency chain.
- Why `Depends(get_current_user)` is a dependency declaration rather than a manual function call.
- How `yield` allows a dependency to provide a value and then run cleanup code.
- Why `try/finally` is used for cleanup.
- How an admin dependency can reuse current-user context.
- Why a failed role check can raise HTTP 403.
- How `app.dependency_overrides` replaces a dependency during tests.
- How `TestClient` and pytest assertions test an endpoint.

The progression is:

```text
Day 8: reusable dependencies
          ↓
Day 9: dependency chains
          ↓
       yield + cleanup
          ↓
       dependency overrides
          ↓
       endpoint testing
```

# 2. Day 8 Recap

On Day 8, you used `Depends()` for current-user context and pagination. For example:

```python
@router.get("/current_user")
async def profile(current_user=Depends(get_current_user)):
    ...
```

The endpoint declares that it needs a user value. FastAPI resolves `get_current_user` and supplies its result to `current_user`.

Your pagination dependency is separate:

```python
from fastapi import Query

async def pagination(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    return {"page": page, "limit": limit}
```

The pagination dependency extracts and validates query parameters; the product/order service applies the values to the filtered collection. Day 9 builds on these ideas rather than replacing the existing filters or pagination logic.

# 3. What Is a Sub-dependency?

A **sub-dependency** is a dependency that another dependency itself requires.

Your admin dependency declares:

```python
async def is_admin(admin=Depends(get_current_user)):
    ...
```

Here `is_admin` is a dependency, and `get_current_user` is a dependency used by it. Therefore, `get_current_user` is a sub-dependency in this chain.

The request flow is:

```text
GET /profile/is_admin
        ↓
endpoint depends on is_admin
        ↓
is_admin depends on get_current_user
        ↓
current-user dictionary is provided
        ↓
role is checked
        ↓
admin context is yielded OR HTTP 403 is raised
```

## 3.1 Why it is useful

An e-commerce API might restrict product creation, updating, and deletion to administrators. Repeating the same role check in every endpoint creates duplication. A reusable authorization dependency centralizes that check, while each endpoint simply declares that it needs the authorized context.

A dependency should still have one focused responsibility. Do not make `is_admin()` calculate prices, update products, or perform every business operation.

# 4. Dependency Files in Your Project

Your Day 9 project includes:

```text
day_9/
├── dependencies/
│   ├── current_user.py
│   ├── admin.py
│   └── pagination.py
├── routers/
│   ├── profile.py
│   ├── products.py
│   └── orders.py
├── services/
│   ├── profile.py
│   ├── products.py
│   └── orders.py
├── tests/
│   └── test_profile.py
└── main.py
```

| File | Responsibility in this lesson |
|---|---|
| `dependencies/current_user.py` | Provides mock user context and demonstrates `yield` cleanup. |
| `dependencies/admin.py` | Reuses current-user context and checks the role. |
| `dependencies/pagination.py` | Extracts and validates pagination parameters. |
| `routers/profile.py` | Defines profile, status, and admin-check routes. |
| `services/profile.py` | Builds the profile response and checks account status. |
| `tests/test_profile.py` | Overrides the current-user dependency and tests the profile route. |

# 5. Your `get_current_user()` Dependency

**File:** `dependencies/current_user.py`

## 5.1 Implemented code

```python
async def get_current_user():
    try:
        yield {
            "id": 101,
            "user_name": "venkat",
            "role": "Admin",
            "status": "Active"
        }
    finally:
        print("Current user check completed")
```

## 5.2 Line-by-line explanation

### `async def get_current_user():`

Defines an asynchronous dependency provider. FastAPI can resolve it while processing a request.

### `try:`

Begins a `try` block that contains the dependency's value-providing step. The `finally` block below is used for cleanup.

### `yield { ... }`

The yielded dictionary is the current project's mock user:

```python
{
    "id": 101,
    "user_name": "venkat",
    "role": "Admin",
    "status": "Active"
}
```

- `id`: mock user identifier.
- `user_name`: username.
- `role`: value used by the admin dependency.
- `status`: value used by the account-status service.

With a FastAPI dependency using `yield`, FastAPI provides the yielded value to the endpoint or dependent dependency, then resumes the dependency lifecycle so cleanup code can run.

### `finally:`

Python executes the `finally` block when control exits the associated `try` construct, including when an exception occurs.

### `print("Current user check completed")`

This is a simple cleanup demonstration. Your current code has no database session or other resource to release, so it prints a message instead.

# 6. `yield` Versus `return`

A normal dependency can use `return` when it only needs to supply a value:

```python
async def simple_current_user():
    return {
        "id": 101,
        "user_name": "venkat",
        "role": "Admin",
        "status": "Active"
    }
```

The function returns a value and finishes. It does not create the same setup/use/cleanup pattern as a yield-based dependency.

A yield-based dependency can provide a value and then execute cleanup:

```python
async def get_value():
    try:
        yield {"message": "Hello"}
    finally:
        print("Cleanup completed")
```

Think of the lifecycle as:

```text
dependency starts
       ↓
prepare value/resource
       ↓
yield value to FastAPI
       ↓
endpoint/dependent operation runs
       ↓
dependency resumes
       ↓
finally cleanup runs
```

`yield` is useful when there is real cleanup work, such as closing a database session later in the roadmap. Do not convert every dependency to `yield` without a reason.

# 7. Why `try/finally` Is Used

Your code uses this pattern:

```python
try:
    yield {...}
finally:
    print("Current user check completed")
```

The purpose of `finally` is to keep cleanup code from being skipped just because the operation exits through an exception. For a future database dependency, the cleanup might close a session. In your current example, it only prints a message.

`finally` guarantees that Python enters the cleanup block when leaving the `try`; it does not guarantee that the cleanup code itself cannot fail. The cleanup operation must still be implemented correctly.

# 8. Your `is_admin()` Dependency

**File:** `dependencies/admin.py`

## 8.1 Implemented code

```python
from dependencies.current_user import get_current_user
from fastapi import Depends, HTTPException

async def is_admin(admin=Depends(get_current_user)):
    try:
        if admin["role"] != "Admin":
            raise HTTPException(
                status_code=403,
                detail={
                    "message": "Admin required"
                }
            )
        yield admin
    finally:
        print("Admin check completed")
```

## 8.2 Imports

```python
from dependencies.current_user import get_current_user
```

Makes the dependency function available in this module. Importing the function does not itself resolve it for an HTTP request.

```python
from fastapi import Depends, HTTPException
```

- `Depends` declares that `is_admin` requires another dependency.
- `HTTPException` allows the dependency to stop a request with an HTTP error.

## 8.3 The sub-dependency parameter

```python
async def is_admin(admin=Depends(get_current_user)):
```

FastAPI resolves `get_current_user` and supplies its yielded value to the parameter named `admin`. In this project that value is the user dictionary.

The variable is named `admin`, but at the start of the function it is the user context being checked. A future readability refactor could rename it to `current_user`; these notes preserve the actual code.

## 8.4 Role check

```python
if admin["role"] != "Admin":
```

The condition checks whether the role differs from `Admin`. If it does, the function raises an HTTP exception.

## 8.5 HTTP 403

```python
raise HTTPException(
    status_code=403,
    detail={"message": "Admin required"}
)
```

HTTP 403 means the server understood the request but refuses to authorize the operation. Because the exception is raised, execution does not reach `yield admin` on the failed path.

## 8.6 Yielding the approved context

```python
yield admin
```

If the role check succeeds, the dependency yields the user dictionary to the endpoint. The endpoint can use that context without repeating the role check.

## 8.7 Cleanup

```python
finally:
    print("Admin check completed")
```

This demonstrates cleanup for the `is_admin()` dependency lifecycle.

# 9. The `/profile/is_admin` Route

**File:** `routers/profile.py`

Your implemented route is:

```python
@router.get("/is_admin")
async def is_user_admin(is_admin=Depends(is_admin)):
    return is_admin
```

In `main.py`, the profile router is included with the prefix `/profile`, so the full route is `GET /profile/is_admin`.

The `Depends(is_admin)` expression refers to the imported dependency function. FastAPI resolves it, and the parameter named `is_admin` receives its yielded value. The parameter name shadows the imported name inside the function body, which is valid Python, but a distinct parameter name can make the code easier to read:

```python
@router.get("/is_admin")
async def is_user_admin(admin_user=Depends(is_admin)):
    return admin_user
```

That is an optional readability improvement, not a different concept.

## Request flow

```text
GET /profile/is_admin
          ↓
FastAPI resolves is_admin()
          ↓
FastAPI resolves get_current_user()
          ↓
mock user dictionary is yielded
          ↓
is_admin checks the role
          ├── role is Admin → yields user dictionary → route returns it
          └── another role → raises HTTP 403
```

Your normal mock user has role `Admin`, so the role check passes during normal application behavior.

# 10. The Current-user Profile Route

**File:** `routers/profile.py`

```python
from dependencies.current_user import get_current_user
from dependencies.admin import is_admin
from fastapi import Depends, APIRouter
from services.profile import get_user_profile, account_active_status

router = APIRouter()

@router.get("/current_user")
async def profile(current_user=Depends(get_current_user)):
    profile = await get_user_profile(current_user)
    return profile
```

- `APIRouter()` groups related routes.
- `Depends(get_current_user)` asks FastAPI to resolve the dependency.
- The yielded dictionary is assigned to `current_user`.
- `await get_user_profile(current_user)` calls the asynchronous service.
- `return profile` sends the service result back as the response.

The separation is:

```text
get_current_user → provides user context
profile router   → handles HTTP route and orchestration
profile service  → builds the profile response
```

# 11. Account-status Validation in the Service Layer

Your profile router also includes:

```python
@router.get("/status")
async def account_status(current_user=Depends(get_current_user)):
    status = await account_active_status(current_user)
    return status
```

**File:** `services/profile.py`

```python
from fastapi import HTTPException

async def account_active_status(current_user):
    if current_user["status"] != "Active":
        raise HTTPException(
            status_code=403,
            detail={"message": "Only active users can login"}
        )
    return current_user
```

This service checks the user's status, not their role:

- `is_admin()` checks whether `role == "Admin"`.
- `account_active_status()` checks whether `status == "Active"`.

A user could be an admin and still be inactive; an active user could be a non-admin. Your current mock dictionary has both `role: "Admin"` and `status: "Active"`.

This is how your project is currently organized: account-status checking is in the service layer, while the admin check is a dependency. Do not move code merely to make every check use the same layer. Later, if many routes need the same precondition, you can evaluate whether it should become a reusable dependency.

# 12. Dependency Overrides

FastAPI's `app.dependency_overrides` dictionary lets a test replace a dependency provider with another callable. This is useful when the normal dependency has fixed mock data or relies on infrastructure that a test should not need.

Your test defines:

```python
def fake_current_user():
    return {
        "id": 999,
        "user_name": "test_user",
        "role": "User",
        "status": "Active"
    }
```

This is a controlled test user. It has ID `999` and role `User`, rather than the normal mock user's ID `101` and role `Admin`.

The override is registered using:

```python
app.dependency_overrides[get_current_user] = fake_current_user
```

The dictionary key is the original dependency function object, not the string name. The value is the replacement callable. When FastAPI resolves `get_current_user` for the test request, it uses `fake_current_user` instead.

The original function is not rewritten. The override changes which callable FastAPI resolves in the test app.

# 13. Your Day 9 pytest Test

**File:** `tests/test_profile.py`

```python
from fastapi.testclient import TestClient

from main import app
from dependencies.current_user import get_current_user


def fake_current_user():
    return {
        "id": 999,
        "user_name": "test_user",
        "role": "User",
        "status": "Active"
    }


app.dependency_overrides[get_current_user] = fake_current_user

client = TestClient(app)


def test_profile():
    response = client.get("/profile/current_user")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 999
    assert data["user_name"] == "test_user"
    assert data["role"] == "User"

    app.dependency_overrides = {}
```

## 13.1 Imports

`TestClient` sends requests to the FastAPI app during testing. Importing `app` gives the test the application with its routers and middleware. Importing `get_current_user` gives the test the exact callable it wants to override.

## 13.2 Create the client

```python
client = TestClient(app)
```

This lets the test call the app without starting a separate web server.

## 13.3 Send the request

```python
response = client.get("/profile/current_user")
```

This sends a GET request through the FastAPI application. Since the override is active, the profile route should receive the fake test user.

## 13.4 Assert the HTTP status

```python
assert response.status_code == 200
```

The test expects the endpoint to succeed with HTTP 200. If it returns another status code, pytest fails the assertion.

## 13.5 Parse JSON

```python
data = response.json()
```

This converts the JSON response body into a Python dictionary, allowing the test to inspect fields by key.

## 13.6 Assert the expected values

```python
assert data["id"] == 999
assert data["user_name"] == "test_user"
assert data["role"] == "User"
```

These checks verify that the response contains the replacement user's data rather than the original mock user's values.

## 13.7 Clear the override

```python
app.dependency_overrides = {}
```

This clears all overrides in the app, not just the one for `get_current_user`. It works for this small example, but in a larger suite it may accidentally remove another test's override. A safer pattern restores only the dependency changed:

```python
app.dependency_overrides[get_current_user] = fake_current_user

try:
    response = client.get("/profile/current_user")
    assert response.status_code == 200
finally:
    app.dependency_overrides.pop(get_current_user, None)
```

The `finally` block runs even if the assertion fails. A pytest fixture is also a good cleanup mechanism as the test suite grows. This is an improvement pattern; your original code clears the whole dictionary.

# 14. How the Test Request Flows

```text
pytest starts test_profile()
          ↓
TestClient sends GET /profile/current_user
          ↓
FastAPI matches the profile route
          ↓
FastAPI sees Depends(get_current_user)
          ↓
FastAPI checks dependency_overrides
          ↓
fake_current_user() supplies the test dictionary
          ↓
profile router receives current_user
          ↓
get_user_profile(current_user) builds response
          ↓
FastAPI returns HTTP 200 + JSON
          ↓
pytest checks status and JSON fields
```

A passing test supports these claims: the route can be called by the test client, the override provides the test user, the response status is 200, and the asserted JSON fields match. It does **not** prove real authentication or JWT verification works, because the dependency is replaced in the test.

# 15. Running the Test

Run commands from the **Day 9 project directory**, where `main.py`, `dependencies/`, `routers/`, `services/`, and `tests/` are located. Activate the Day 9 project's own virtual environment, not another day's or the parent folder's environment.

Run the specific test:

```bash
pytest -v tests/test_profile.py
```

Or run all tests:

```bash
pytest -v
```

A passing output should contain a line similar to:

```text
tests/test_profile.py::test_profile PASSED
```

The exact duration and output can vary. Do not mark the test as passing until pytest actually reports success. If imports fail, check that the terminal is in the project folder, the correct virtual environment is active, dependencies are installed in that environment, and the expected files/folders exist.

# 16. Day 9 Architecture Overview

```text
                         main.py
                            |
                            v
                      profile router
                       /           \
                      v             v
           get_current_user       is_admin
                      ^             |
                      |             v
                      +------ get_current_user
                                    |
                                    v
                              role validation
                                    |
                        +-----------+-----------+
                        |                       |
                        v                       v
                   role Admin               other role
                        |                       |
                        v                       v
                 yield user context          HTTP 403
                        |
                        v
                     endpoint
                        |
                        v
                 profile service
                        |
                        v
                  JSON response
```

Testing introduces a replacement boundary:

```text
test_profile.py
      |
      v
app.dependency_overrides
      |
      +-- get_current_user → fake_current_user
                                  |
                                  v
                           test user dictionary
                                  |
                                  v
                            profile endpoint
                                  |
                                  v
                         response assertions
```

# 17. Day 8 Versus Day 9

| Area | Day 8 | Day 9 |
|---|---|---|
| Main focus | Reusable dependency injection | Dependency composition, lifecycle, and tests |
| Example | Current-user provider | Admin dependency depending on current-user provider |
| Pagination | Shared validated parameters | Existing pagination dependency remains in place |
| Lifecycle | Basic dependency resolution | `yield` and `finally` cleanup |
| Authorization | Current-user context is provided | Role check in `is_admin()` |
| Testing | Testing benefits explained | `dependency_overrides` and `TestClient` test |
| Proof | FastAPI injects a dependency result | Test replaces provider and verifies returned data |

# 18. Common Mistakes and Important Distinctions

## 18.1 Import versus execution

```python
from dependencies.current_user import get_current_user
```

makes the function available. It does not itself run the dependency for every HTTP request.

```python
Depends(get_current_user)
```

declares that FastAPI should resolve the dependency.

## 18.2 Direct dependency versus sub-dependency

If a route uses `Depends(get_current_user)`, that is a direct dependency of the route. If `is_admin` uses `Depends(get_current_user)`, then `get_current_user` is a sub-dependency in that chain.

## 18.3 `yield` versus `return`

`return` supplies a value and ends the function. `yield` pauses a generator and enables FastAPI to manage a dependency's setup/use/cleanup lifecycle.

## 18.4 HTTP 401 versus 403

- **401 Unauthorized:** generally means valid authentication credentials are missing or invalid.
- **403 Forbidden:** means the server refuses to authorize the operation.

Your role check uses 403 when the supplied user's role is not `Admin`.

## 18.5 Mock user versus real authentication

Your `get_current_user()` currently returns a fixed dictionary. It does not inspect a bearer token, validate a JWT, check a password, or query a user table. This is intentional for this learning stage; real authentication belongs later in the roadmap.

## 18.6 Override versus modifying the original function

The override does not rewrite `get_current_user()`. It instructs FastAPI to use a replacement callable when resolving that dependency in the test application.

## 18.7 Do not overstate test coverage

The current test calls `/profile/current_user`. It does not test `/profile/status`, `/profile/is_admin`, product CRUD, order CRUD, or the 403 branch of the admin dependency.

## 18.8 Avoid broad cleanup in a large test suite

Clearing `app.dependency_overrides` removes every override. Prefer restoring only the override you changed or using a pytest fixture.

## 18.9 Keep responsibilities focused

Dependencies provide reusable context or preconditions. The profile service builds the profile response; product/order services keep their business logic. Do not move every business function into a dependency just because `Depends()` exists.

# 19. What This Implementation Does and Does Not Prove

## Implemented in your project

- `get_current_user()` yields a mock user dictionary.
- Its `finally` block prints a cleanup message.
- `is_admin()` depends on `get_current_user()`.
- `is_admin()` checks the role and raises HTTP 403 for a non-admin role.
- `/profile/current_user` injects current-user context into the profile router.
- `/profile/status` sends current-user context to the account-status service.
- `/profile/is_admin` uses the admin dependency.
- The test overrides `get_current_user()`.
- The test calls `/profile/current_user` through `TestClient`.
- The test asserts the response status and selected user fields.

## Not implemented by this Day 9 code

- Password verification.
- JWT creation or verification.
- Bearer-token authentication.
- Database-backed user lookup.
- Database session dependency.
- Dynamic permissions or database-driven RBAC.
- A test specifically asserting that `/profile/is_admin` returns 403 for a non-admin user.

These are outside this day's implementation scope, not reasons to rewrite the project now.

# 20. Revision Questions

Try answering without looking at the previous sections:

1. What makes `get_current_user()` a sub-dependency of `is_admin()`?
2. What is the difference between `Depends(get_current_user)` and calling the function manually?
3. What dictionary does `get_current_user()` yield in this project?
4. Why is `yield` useful when a dependency has cleanup work?
5. What is the purpose of `finally`?
6. What does `is_admin()` check?
7. Why does the admin dependency raise HTTP 403?
8. What is the difference between role and account status?
9. What does `app.dependency_overrides` do?
10. Why does the test import the original `get_current_user` function?
11. What does `TestClient` allow you to do?
12. Why does the test expect `data["id"] == 999` instead of `101`?
13. Which endpoint does the current test call?
14. Does this test prove JWT authentication works? Why or why not?
15. Why might clearing every dependency override be unsafe in a larger test suite?

# 21. Day 9 Completion Checklist

- [x] Understand what a sub-dependency is.
- [x] Implement `is_admin()` using `Depends(get_current_user)`.
- [x] Understand how FastAPI resolves the dependency chain.
- [x] Use `yield` in `get_current_user()`.
- [x] Understand the `try/finally` cleanup pattern.
- [x] Use HTTP 403 for a failed admin-role check.
- [x] Use the admin dependency from `/profile/is_admin`.
- [x] Keep the current-user profile operation in the service layer.
- [x] Use `app.dependency_overrides` in a test.
- [x] Create a fake user for testing.
- [x] Send a request through `TestClient`.
- [x] Assert the response status and JSON values.
- [x] Understand what the test proves and does not prove.
- [ ] Re-run `pytest -v tests/test_profile.py` and confirm a passing result in the current environment, if you have not done so after the latest project changes.
- [ ] Practise testing the non-admin branch of `/profile/is_admin` as a separate exercise.

# 22. Final Mental Model

```text
DEPENDENCY CHAIN

get_current_user()
    | yields user context
    v
is_admin()
    | checks role
    +-- Admin role → yields user context → protected endpoint
    +-- other role → HTTP 403

TESTING

app.dependency_overrides
    | replaces get_current_user
    v
fake_current_user()
    | returns controlled test user
    v
TestClient request
    | exercises endpoint
    v
pytest assertions
```

> **Main lesson:** Dependency injection is not only about reusing functions. It also lets you compose request requirements, manage resource lifecycles, and replace dependencies in tests.

Your Day 9 e-commerce project demonstrates these ideas using current-user context, an admin-role dependency, `yield`/`finally`, and a profile endpoint test. The user identity is still mocked at this stage; real authentication and database-backed authorization will be added at their planned roadmap stages.
