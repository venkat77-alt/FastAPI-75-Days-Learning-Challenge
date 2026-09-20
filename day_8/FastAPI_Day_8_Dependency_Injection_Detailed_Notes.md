# FastAPI Day 8 - Dependency Injection
## Professional Notes, Current Project Implementation, and Long-Term DI Reference

> **Roadmap:** Day 8 - Dependency Injection Essentials  
> **Current implementations:** Current-user profile + pagination  
> **Purpose:** Understand not only *how* to write `Depends()`, but *where* Dependency Injection makes architectural sense in real FastAPI systems.

---

# 1. What Day 8 Is Really About

Day 8 is not about adding `Depends()` everywhere.

The real goal is to develop an engineering instinct:

> **When an endpoint needs something, should the endpoint obtain it itself, should FastAPI provide it through Dependency Injection, or does the responsibility belong somewhere else such as middleware, configuration, a service, or a repository?**

The most important things to understand are:

1. Inversion of Control (IoC)
2. Dependency Injection (DI)
3. FastAPI `Depends()`
4. Normal import vs function call vs DI
5. Dependency resolution
6. Reusable request dependencies
7. Current-user context
8. Pagination
9. Router/dependency/service boundaries
10. Real-world DI application areas
11. When DI should **not** be used

---

# 2. The Three Things You Must Not Confuse

A large amount of beginner confusion comes from treating these as the same thing:

```text
import
function call
Dependency Injection
```

They are different.

---

## 2.1 Normal Import

Example:

```python
from dependencies.current_user import get_current_user
```

What does this do?

It makes the function name available in the current Python file.

Conceptually:

```text
current_user.py
      |
      | contains
      v
get_current_user

profile.py
      |
      | import
      v
can now refer to get_current_user
```

### Important

**Importing a function does not mean your endpoint has received its result.**

You have only made the function available.

---

# 3. Normal Function Call

After importing:

```python
from dependencies.current_user import get_current_user
```

you can explicitly call:

```python
current_user = await get_current_user()
```

Now your code controls the execution.

### Flow

```text
Your endpoint
     |
     | explicitly calls
     v
get_current_user()
     |
     v
result
     |
     v
current_user
```

The important point is:

> **You are controlling when the function runs and how its result is obtained.**

---

## 3.1 Example

```python
from dependencies.current_user import get_current_user

@router.get("/")
async def profile():
    current_user = await get_current_user()

    return current_user
```

Here, the endpoint itself is responsible for calling the provider.

---

# 4. Dependency Injection with FastAPI

Now compare:

```python
from dependencies.current_user import get_current_user
from fastapi import Depends

@router.get("/")
async def profile(
    current_user = Depends(get_current_user)
):
    return current_user
```

This means:

> **FastAPI, this endpoint requires the result of `get_current_user`. Resolve that dependency for this request and inject the result into `current_user`.**

The endpoint declares its requirement instead of explicitly obtaining it.

---

# 5. Import vs Call vs DI - The Exact Difference

| Concept | Code | Who controls execution? | What you get |
|---|---|---|---|
| Import | `from x import get_user` | Python import system | Function reference |
| Normal call | `await get_user()` | Your endpoint/code | Function result |
| DI | `Depends(get_user)` | FastAPI dependency system | Injected function result |

### Mental model

```text
IMPORT

"Make this function available."


CALL

"Run this function now and give me its result."


DI

"FastAPI, this endpoint needs this result.
You resolve the dependency and inject it."
```

This distinction is one of the most important Day 8 concepts.

---

# 6. Why DI Is Useful

Imagine 20 protected endpoints.

Without DI, routes might repeatedly contain:

```python
token = ...
user = ...
validate_token(...)
find_user(...)
```

With DI:

```python
current_user = Depends(get_current_user)
```

Every endpoint declares the requirement.

The authentication implementation can evolve separately.

The endpoint focuses on its actual operation.

### The architectural benefit

```text
Without DI

Endpoint
  |
  +-- obtain dependency
  +-- validate dependency
  +-- business operation
  +-- response


With DI

FastAPI
  |
  +-- resolve dependency
  |
  v
Endpoint
  |
  +-- business operation
  +-- response
```

---

# 7. IoC vs DI vs `Depends()`

### IoC - Inversion of Control

A broad architectural principle:

> Control over how a required component is obtained is moved away from the component that uses it.

### DI - Dependency Injection

A technique for implementing that principle:

> A required dependency is supplied to the component instead of the component manually constructing or locating it.

### `Depends()`

FastAPI's mechanism for declaring a dependency.

```python
current_user = Depends(get_current_user)
```

### In one sentence

```text
IoC = principle
DI  = technique
Depends() = FastAPI mechanism
```

---

# 8. What Is a Dependency?

A dependency is something an endpoint needs before it can perform its operation.

Common examples:

```text
Current authenticated user
Database session
Tenant / organization
Permission context
Pagination parameters
External service client
Feature-flag context
Idempotency context
Request-scoped policy
```

A dependency should have a **focused responsibility**.

---

# 9. Not Every Reusable Function Is a Dependency

This is a critical professional rule.

A function can be reusable without being a dependency.

### Business logic

```python
async def calculate_order_total(items):
    ...
```

This is normally service/domain logic.

### Data processing

```python
def calculate_discount(price, percentage):
    ...
```

This is normally a utility/business rule.

### Dependency

```python
async def get_current_user():
    ...
```

This is a dependency because it provides request-specific context required by an endpoint.

---

# 10. When Should I Use `Depends()`?

Ask these questions:

### Question 1

Does the endpoint need something that has to be obtained, resolved, prepared, or validated before the operation?

If yes, DI may fit.

### Question 2

Is the requirement request-specific?

Examples:

```text
current user
tenant
database session
permissions
pagination
```

If yes, DI is a strong candidate.

### Question 3

Will multiple endpoints need the same resolution logic?

If yes, DI becomes more valuable.

### Question 4

Is it actually business logic?

If yes, keep it in the service/domain layer.

### Question 5

Does it apply to almost every request globally?

If yes, middleware may be more appropriate.

---

# 11. Middleware vs DI

Our project already uses middleware for request-wide work.

Typical middleware responsibilities:

```text
Request timing
Request ID
Central request logging
Response headers
Request/response interception
```

These happen around requests.

DI is better for requirements that a particular endpoint or group of endpoints **needs as an input/context**.

Examples:

```text
Current user
Database session
Tenant
Permission
Pagination
```

### Simple rule

```text
Middleware
"Process the request."

Dependency
"Provide something this operation needs."
```

This is a guideline, not an absolute law.

---

# 12. Current Project Structure

```text
day_8/
├── main.py
├── routers/
│   ├── products.py
│   ├── orders.py
│   └── profile.py
├── services/
│   ├── products.py
│   ├── orders.py
│   └── profile.py
├── schemas/
├── dependencies/
│   ├── current_user.py
│   └── pagination.py
├── Middleware/
├── Exception_handler/
└── config/
```

The new architectural layer is:

```text
dependencies/
```

It contains focused providers of request-specific or infrastructure-related context.

---

# 13. Real Day 8 Example 1 - Current User

## Dependency

```python
async def get_current_user():
    return {
        "id": 101,
        "user_name": "venkat",
        "role": "Admin"
    }
```

This is intentionally a temporary/mock source for Day 8.

The real JWT/current-user implementation belongs later in the roadmap.

---

# 14. Profile Router

```python
from dependencies.current_user import get_current_user
from fastapi import Depends, APIRouter
from services.profile import get_user_profile

router = APIRouter()

@router.get("/")
async def profile(
    current_user = Depends(get_current_user)
):
    profile = await get_user_profile(current_user)
    return profile
```

### What FastAPI does

Request:

```text
GET /current_user_profile/
```

FastAPI sees:

```python
Depends(get_current_user)
```

It resolves:

```python
get_current_user()
```

The result is injected into:

```python
current_user
```

Then:

```python
await get_user_profile(current_user)
```

passes the context to the service.

---

# 15. Profile Service

```python
async def get_user_profile(current_user):
    return {
        "id": current_user["id"],
        "user_name": current_user["user_name"],
        "role": current_user["role"],
        "profile": {
            "name": "venkat",
            "email": "venkat@gmail.com",
            "Mobile number": 9887654321
        }
    }
```

### Responsibility split

```text
get_current_user()
    |
    +-- identify/provide the current user


profile router
    |
    +-- HTTP orchestration


get_user_profile()
    |
    +-- profile business/application logic
```

This is a strong DI example because the endpoint genuinely needs the authenticated-user context.

---

# 16. Why We Did Not Put Everything Inside the Dependency

Avoid turning this:

```python
async def get_current_user():
    ...
```

into a giant operation that also:

```text
loads profile
calculates statistics
generates notifications
checks unrelated business rules
formats the final response
```

Better:

```text
Dependency
    ↓
provide current user context

Service
    ↓
perform profile operation
```

Focused dependencies scale better.

---

# 17. How This Evolves on Day 31

Day 8:

```text
get_current_user()
       ↓
mock user
```

Later:

```text
Bearer token
       ↓
JWT validation
       ↓
identify user
       ↓
database lookup
       ↓
actual user
       ↓
get_current_user()
       ↓
profile endpoint
```

The profile endpoint's dependency boundary stays conceptually stable.

This is an example of designing against a responsibility rather than against today's implementation.

---

# 18. Real Day 8 Example 2 - Pagination

Dependency:

```python
from fastapi import Query

async def get_pagination(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    return {
        "page": page,
        "limit": limit
    }
```

This dependency has a focused responsibility:

> Extract and validate reusable pagination parameters.

It does **not** perform product business logic.

---

# 19. How Pagination DI Works

Request:

```text
GET /products/?page=2&limit=5
```

FastAPI obtains:

```text
page = 2
limit = 5
```

Dependency returns:

```python
{
    "page": 2,
    "limit": 5
}
```

FastAPI injects that result into:

```python
pagination
```

So:

```python
pagination = Depends(get_pagination)
```

does not mean:

> "Paginate the products."

It means:

> "Resolve the pagination parameters and give them to the endpoint."

---

# 20. Product Router with Pagination

Our existing filters remain where they were.

```python
@router.get("/", response_model=list[productsResponse])
async def get_products(
    search: str | None = None,
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    pagination=Depends(get_pagination)
):
    product = await get_products_service(
        search,
        category,
        min_price,
        max_price,
        pagination
    )

    return product
```

### Why we kept the existing filters

The current:

```text
search
category
min_price
max_price
```

implementation was already clear and useful.

We did not move it into another dependency merely to create more `Depends()` examples.

That is deliberate engineering judgment.

---

# 21. Where Pagination Is Actually Used

Inside the service, after filtering:

```python
page = pagination["page"]
limit = pagination["limit"]

start = (page - 1) * limit
end = start + limit

return filtered_product[start:end]
```

### Example

```text
page = 2
limit = 5

start = (2 - 1) * 5 = 5
end = 5 + 5 = 10
```

So:

```python
filtered_product[5:10]
```

returns the second page.

---

# 22. Why Pagination Is Not Used on `/{id}`

Correct:

```text
GET /products/?page=2&limit=10
GET /orders/?page=3&limit=20
```

These return collections.

Not appropriate:

```text
GET /products/5?page=2
GET /orders/10?page=3
```

Those identify one resource.

Therefore pagination was removed from:

```text
GET /products/{id}
GET /orders/{order_id}
```

A professional engineer does not apply an abstraction simply because the abstraction exists.

---

# 23. E-commerce - Where DI Can Be Used

## 23.1 Current User

```text
GET /me/orders
PUT /me/profile
GET /me/cart
```

Dependency:

```text
get_current_user
```

Why:

The endpoint needs to know who the customer is.

---

## 23.2 Database Session

```text
GET /products
POST /orders
PUT /cart
```

Dependency:

```text
get_db
```

Why:

The route needs a request-scoped database session.

Typical lifecycle:

```text
request
  ↓
create session
  ↓
endpoint/service
  ↓
commit/rollback as appropriate
  ↓
close session
```

---

## 23.3 Permission / Admin Context

```text
POST /products
DELETE /products/{id}
```

Dependency:

```text
require_admin
```

Why:

The operation requires authorization before business execution.

---

## 23.4 Tenant/Store Context

For marketplace or multi-store systems:

```text
get_current_store
```

The endpoint may need to know which store/merchant is active.

---

## 23.5 Pagination

Catalog listing:

```text
get_pagination
```

The dependency provides validated parameters; the service/repository performs the query.

---

# 24. FinTech - Where DI Can Be Used

Financial systems often need strong request-scoped context.

## 24.1 Authenticated Customer

```text
current_user = Depends(get_current_user)
```

Used for:

```text
accounts
transfers
statements
beneficiaries
```

---

## 24.2 Active Account Context

```text
account = Depends(get_active_account)
```

The dependency can establish that the requested account belongs to the caller and is usable.

The transfer service then focuses on the financial operation.

---

## 24.3 Idempotency Context

```text
get_idempotency_context
```

Useful for operations where retries must not create duplicate transactions.

Flow:

```text
Idempotency key
    ↓
dependency validates/loads request context
    ↓
service executes transaction
```

---

## 24.4 Authorization Context

A high-risk operation may need:

```text
current user
account ownership
transaction policy
permission
```

These are good dependency boundaries.

The actual financial business rules remain in the service/domain layer.

---

## 24.5 External Payment/Banking Client

```text
payment_client = Depends(get_payment_client)
```

This can make the real integration replaceable in tests.

---

# 25. Healthcare - Where DI Can Be Used

Healthcare systems often need multiple layers of request-specific context.

## 25.1 Authorized Patient Context

```text
patient = Depends(get_authorized_patient)
```

The dependency can establish:

```text
identity
patient existence
access eligibility
organization/facility scope
```

Then the service retrieves the requested data.

---

## 25.2 Clinician Context

```text
clinician = Depends(get_current_clinician)
```

Useful when operations require clinician identity or scope.

---

## 25.3 Facility / Organization Context

For hospital systems:

```text
facility = Depends(get_current_facility)
```

Useful when the same API serves multiple facilities.

---

## 25.4 Database Session

Medical record endpoints may use a request-scoped DB session through DI.

---

## 25.5 Audit Context

Universal HTTP logging can remain middleware.

Business-level audit context can be assembled through dependencies when an operation needs user/patient/facility information.

---

# 26. SaaS / Multi-Tenant - Where DI Can Be Used

This is one of the strongest areas for DI.

## 26.1 Current Organization

```text
tenant = Depends(get_current_tenant)
```

Why:

A large number of operations must execute inside one organization.

```text
Request
  ↓
current user
  ↓
organization membership
  ↓
tenant context
  ↓
service
```

---

## 26.2 Permissions

```text
PermissionChecker("reports:export")
```

This is a later-roadmap pattern.

It may depend on:

```text
current user
    ↓
organization
    ↓
membership
    ↓
role
    ↓
permission
```

That is dependency composition.

---

## 26.3 Feature Flags

```text
feature_context = Depends(get_feature_context)
```

Useful when feature access depends on tenant/user/application configuration.

---

# 27. Custom Enterprise Software

"Custom software" is not a single DI pattern.

The best DI candidates usually appear at boundaries between:

```text
HTTP
identity
organization
authorization
database
external systems
business services
```

Examples:

```text
Current employee
Current department
Tenant
DB session
External service client
Policy context
Workflow context
```

---

# 28. Logistics / Delivery

Useful dependencies:

```text
get_current_driver
get_company_context
get_shipment
get_authorized_shipment
get_db
get_pagination
```

Example flow:

```text
PUT /shipments/{id}/status
        ↓
current driver
        ↓
authorized shipment
        ↓
shipment service
```

The dependency establishes request context; the service changes shipment state.

---

# 29. Education

Potential DI areas:

```text
current student
current teacher
institution
course membership
permission
database session
```

Example:

```text
GET /courses/{course_id}/materials
        ↓
current user
        ↓
course membership
        ↓
service
```

The service then handles the actual material retrieval rules.

---

# 30. Media / Subscription Systems

Potential dependencies:

```text
current subscriber
subscription/entitlement
pagination
content policy
```

Example:

```text
GET /premium/videos
        ↓
current subscriber
        ↓
subscription entitlement
        ↓
content service
```

The endpoint should not manually repeat entitlement resolution everywhere.

---

# 31. Travel Systems

Potential dependencies:

```text
current customer
booking context
payment client
availability service
tenant/agency
```

Example:

```text
POST /bookings
    ↓
current customer
    ↓
availability context
    ↓
booking service
```

---

# 32. Manufacturing / Industrial Systems

Potential dependencies:

```text
operator context
plant/facility
equipment context
authorization
DB session
```

Example:

```text
POST /machines/{id}/maintenance
        ↓
authorized operator
        ↓
machine context
        ↓
maintenance service
```

---

# 33. HR / Enterprise Administration

Potential dependencies:

```text
current employee
department
organization
permission
approval context
```

Example:

```text
POST /leave-requests
        ↓
current employee
        ↓
approval policy context
        ↓
leave service
```

---

# 34. External Service Clients

DI can be useful whenever your application depends on an external system.

Examples:

```text
Payment gateway
Email provider
Object storage
SMS provider
Notification provider
Search service
Geocoding service
Internal microservice client
```

Example:

```python
def get_payment_client():
    return PaymentClient(settings.payment_url)

@router.post("/pay")
async def pay(
    payment_client = Depends(get_payment_client)
):
    return await payment_service.pay(payment_client)
```

The important architectural idea is:

```text
router
   ↓
dependency provides client
   ↓
service uses client
```

The service does not need to know how FastAPI constructed the client.

---

# 35. Testing - A Major DI Benefit

Dependency boundaries create seams that tests can replace.

Example:

```python
app.dependency_overrides[get_current_user] = fake_current_user

def fake_current_user():
    return {
        "id": 999,
        "user_name": "test-user",
        "role": "Admin"
    }
```

The test can now exercise the endpoint without relying on real authentication.

The same principle can be used with:

```text
database session
payment client
email provider
external API client
tenant resolver
```

---

# 36. Dependency Caching

FastAPI normally caches a dependency result within a single request.

This matters when the same dependency is required multiple times within that request's dependency graph.

Conceptually:

```text
Request
   ↓
resolve current user
   ↓
reuse current user result
```

This is **request-scoped dependency reuse**.

Do not confuse it with application-level caching such as Redis.

---

# 37. Sub-dependencies and Dependency Chains

Example:

```text
Endpoint
   ↓
PermissionChecker
   ↓
get_current_user
   ↓
database/session
```

One dependency can itself depend on another dependency.

This becomes especially useful for authorization.

### Important roadmap note

Sub-dependencies, chaining, class-based dependencies, `yield`, and dependency overrides are primarily Day 9 material in our 75-day roadmap.

Do not pull all of Day 9 into Day 8 just to make Day 8 look more advanced.

---

# 38. What NOT to Use DI For

Avoid:

### 38.1 Simple business functions

```python
calculate_discount(...)
```

Keep as normal service/domain logic.

### 38.2 Configuration

```text
APP_NAME
SECRET_KEY
DATABASE_URL
```

Keep in the configuration/settings layer.

### 38.3 Universal request processing

If something truly applies to nearly every request, consider middleware.

### 38.4 Giant dependencies

Do not create:

```text
authenticate
+ query five tables
+ calculate business totals
+ update database
+ send email
+ build final response
```

as one dependency.

### 38.5 Artificial abstractions

Do not move code between files just to make a `Depends()` example.

---

# 39. Architecture Decision Cheat Sheet

```text
Question:
"What is this responsibility?"

Identity/context needed by an endpoint
    → Dependency

Database session lifecycle
    → Dependency

Reusable query/request parameter preparation
    → Dependency

Authorization / permission context
    → Dependency

Request-wide timing/logging
    → Middleware

Global error interception
    → Exception handler

Configuration
    → Settings/config layer

Validation/data contract
    → Pydantic schema

Business rules
    → Service/domain layer

Database queries
    → Repository/data-access layer (later roadmap)
```

---

# 40. Day 8 Final Architecture

```text
                 HTTP Request
                      |
                      v
                 Middleware
                      |
                      v
                   Router
                      |
          +-----------+-----------+
          |                       |
          v                       v
   Dependencies            Request inputs
          |
          v
       Service
          |
          v
   Business logic
          |
          v
      Response DTO
          |
          v
        Client
```

The dependency layer is not a replacement for every other layer.

It is a focused boundary for obtaining required context.

---

# 41. Day 8 Checklist

You are ready to mark Day 8 complete when you can explain:

- [x] What IoC means
- [x] What DI means
- [x] What `Depends()` does
- [x] Difference between importing a function and calling it
- [x] Difference between a normal function call and DI
- [x] Why the endpoint receives a dependency result
- [x] Why current-user context is a good DI example
- [x] Why pagination parameters are a good DI example
- [x] Why pagination is applied by the service rather than the dependency
- [x] Why pagination does not belong on `/{id}` lookups
- [x] Why existing product filters were intentionally left in the service
- [x] Difference between middleware and DI
- [x] Where DI can appear in real domains
- [x] Why not every reusable function should become a dependency

---

# 42. Final Mental Model

When building a FastAPI endpoint, think:

```text
1. What does this endpoint need?

2. Is that need request-specific/context-specific?

3. Does it need to be resolved or prepared before the operation?

4. Will multiple endpoints reuse the same resolution logic?

5. Is this actually business logic?

6. Would middleware be a better fit?

7. Can the dependency have one focused responsibility?
```

Then choose the appropriate layer.

### The most important Day 8 sentence

> **Dependency Injection is not about using `Depends()` everywhere. It is about creating clean boundaries around things an operation needs but should not be responsible for obtaining itself.**

---

# 43. Roadmap Progression

```text
DAY 8
IoC
Depends()
Current-user context
Pagination
        ↓
DAY 9
Sub-dependencies
Dependency chaining
Class-based dependencies
Test overrides
yield / cleanup dependencies
        ↓
DAYS 21-35
Authentication + JWT
        ↓
DAY 31
Real get_current_user dependency
        ↓
DAYS 36-37
Admin/User protected operations
        ↓
DAYS 52-53
Dynamic RBAC + granular PermissionChecker
```

The roadmap remains the source of truth. Advanced security and RBAC patterns should be introduced at their planned stages.

---

# 44. One-Page Revision Summary

```text
IMPORT
→ makes a function available

CALL
→ your code explicitly executes the function

DI
→ FastAPI resolves the declared dependency and injects its result

IoC
→ broader principle of reversing control

Depends()
→ FastAPI dependency declaration mechanism

GOOD DI
→ current user
→ DB session
→ tenant
→ permissions
→ pagination
→ external clients

NOT USUALLY DI
→ business calculations
→ ordinary utility functions
→ application configuration
→ universal request processing

DAY 8 IMPLEMENTATIONS
→ current-user profile
→ pagination for collection endpoints

DAY 9
→ dependency composition and lifecycle

DAY 31
→ real authenticated current user

DAY 52-53
→ dynamic RBAC + granular permissions
```
