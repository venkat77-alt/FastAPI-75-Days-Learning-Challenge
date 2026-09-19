# FastAPI Day 7 — Data Transfer Object (DTO) Pattern: Request vs Response Schemas

## 1. Day 7 Overview

Day 7 focuses on designing clear data contracts between a FastAPI application and its clients.

### Topics covered

1. Data Transfer Object (DTO) pattern
2. Request DTO vs Response DTO
3. Pydantic models as DTOs
4. Request/response separation
5. FastAPI `response_model`
6. Response serialization and filtering
7. Nested response DTOs
8. Different response DTOs for different endpoints
9. Sensitive-field masking
10. `response_model_exclude_unset`
11. Difference between `exclude_unset`, `exclude_none`, and `exclude_defaults`
12. `ResponseValidationError`
13. Practical Products, Orders, and Users examples

---

# 2. What Is a DTO?

DTO stands for **Data Transfer Object**.

A DTO is an object used to define the structure of data transferred between different parts of a system.

In FastAPI, Pydantic models commonly implement DTOs.

A DTO is an architectural/data-contract concept. It is not a special FastAPI class.

Example:

```python
from pydantic import BaseModel

class CreateOrderRequest(BaseModel):
    item: str
    quantity: int

class OrderResponse(BaseModel):
    id: int
    item: str
    quantity: int
```

`CreateOrderRequest` is a Request DTO and `OrderResponse` is a Response DTO.

---

# 3. Request DTO vs Response DTO

A Request DTO describes what the API accepts.

A Response DTO describes what the API exposes.

## Request flow

```text
Client JSON
    ↓
Request DTO
    ↓
Validation
    ↓
Python object
    ↓
Service / business logic
```

## Response flow

```text
Service / internal data
    ↓
Response DTO
    ↓
Validation + filtering + serialization
    ↓
JSON response
    ↓
Client
```

### Core rule

> Request DTO = what the API is allowed to receive.

> Response DTO = what the API is allowed to expose.

---

# 4. Why Request and Response Schemas Should Be Separate

Suppose a user creates an account.

The client needs to send a password:

```json
{
    "username": "venkat",
    "password": "Venkat@123"
}
```

The server may internally have:

```python
{
    "id": 1,
    "username": "venkat",
    "password": "Venkat@123",
    "role": "admin"
}
```

But returning the password would be unsafe.

Therefore the request model can contain the password while the response model does not.

```python
from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
```

The request accepts:

```text
username
password
```

The response exposes:

```text
id
username
role
```

---

# 5. Pydantic Models as DTOs

Pydantic models from previous days can already function as DTOs.

For example:

```python
class CreateProduct(BaseModel):
    item: str
    category: str
    price: int
```

When used as API input, this is a Request DTO.

You do not need a special DTO class just because the architecture calls it a DTO.

The important thing is the model's role as a data contract.

---

# 6. Order Request and Response DTO Example

```python
from pydantic import BaseModel

class CreateOrderRequest(BaseModel):
    item: str
    quantity: int

class OrderResponse(BaseModel):
    id: int
    item: str
    quantity: int
```

Request:

```json
{
    "item": "mobile",
    "quantity": 2
}
```

Response:

```json
{
    "id": 1,
    "item": "mobile",
    "quantity": 2
}
```

The client did not provide `id`; the server generated it.

Therefore:

```text
Request DTO  → no id
Response DTO → contains id
```

---

# 7. User Request and Response DTO Example

```python
class CreateUserRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
```

The password is accepted as input but is not exposed as output.

---

# 8. FastAPI `response_model`

`response_model` is a parameter of a FastAPI route decorator.

Example:

```python
@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    ...
```

`response_model=OrderResponse` declares the endpoint's output contract.

FastAPI uses it for response validation, serialization, field filtering, and OpenAPI documentation.

---

# 9. Request Model vs Response Model Placement

Request DTO:

```python
async def create_order(order: CreateOrderRequest):
```

Response DTO:

```python
@router.post("/", response_model=OrderResponse)
```

Together:

```python
@router.post("/", response_model=OrderResponse)
async def create_order(order: CreateOrderRequest):
    ...
```

Mental model:

```text
                    ENDPOINT
                       │
          ┌────────────┴────────────┐
          │                         │
      Request                  Response
          │                         │
CreateOrderRequest             OrderResponse
          │                         │
         IN                        OUT
```

---

# 10. `response_model` Is Endpoint-Specific

Every endpoint can have its own response contract.

Example:

```python
@router.get("/", response_model=list[ProductsResponse])
async def get_products():
    ...
```

A single product:

```python
@router.get("/{id}", response_model=ProductsResponse)
async def get_product(id: int):
    ...
```

User creation:

```python
@router.post("/create/user", response_model=UserCreateResponse)
async def create_user(...):
    ...
```

Login:

```python
@router.post("/login", response_model=LoginResponse)
async def login(...):
    ...
```

There is no rule that all endpoints must use the same response DTO.

---

# 11. `list[ResponseModel]`

For a list response:

```python
@router.get("/", response_model=list[ProductsResponse])
async def get_products():
    ...
```

the response is conceptually:

```text
list
 ├── ProductsResponse
 ├── ProductsResponse
 ├── ProductsResponse
 └── ...
```

For a single object:

```python
@router.get("/{id}", response_model=ProductsResponse)
async def get_product(id: int):
    ...
```

there is no list wrapper.

---

# 12. Nested Response DTOs

A response DTO can contain another Pydantic model.

Example:

```python
class ProductCreateObject(BaseModel):
    id: int
    item: str
    category: str
    price: int
    stock: int
    Discount_price: int
    supplier: Supplier

class ProductCreateResponse(BaseModel):
    message: str
    product: ProductCreateObject
```

Structure:

```text
ProductCreateResponse
│
├── message
│
└── product
    ├── id
    ├── item
    ├── category
    ├── price
    ├── stock
    ├── Discount_price
    └── supplier
```

---

# 13. Products API — Practical Day 7 Example

The project used response schemas similar to:

```python
from pydantic import BaseModel
from schemas.request_schema import suppelier

class productsResponse(BaseModel):
    item: str
    category: str
    price: int
    stock: int
    Discount_price: int

class productcreateobject(BaseModel):
    id: int
    item: str
    category: str
    price: int
    stock: int
    Discount_price: int
    supplier: suppelier

class productcreateresponse(BaseModel):
    message: str
    product: productcreateobject
```

GET product list:

```python
@router.get("/", response_model=list[productsResponse])
async def get_products(...):
    product = await get_products_service(...)
    return product
```

GET one product:

```python
@router.get("/{id}", response_model=productsResponse)
async def get_product(id: int):
    product = await get_product_service(id)

    if product:
        return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )
```

POST product:

```python
@router.post("/", response_model=productcreateresponse)
async def post_product(product: createproduct):
    new_product = await add_product_service(product)

    return {
        "message": "The product created successfully",
        "product": new_product
    }
```

The same internal product can therefore have different public representations.

---

# 14. Response Models Filter Extra Fields

Suppose internal data is:

```python
user = {
    "id": 1,
    "username": "venkat",
    "password": "Venkat@123",
    "role": "admin",
    "email": "venkat@gmail.com",
    "phone": "9876543210",
    "address": "Vijayawada"
}
```

But the response DTO is:

```python
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
```

Then the public response contract contains:

```text
id
username
role
```

It does not expose:

```text
password
email
phone
address
```

The response model therefore acts as an output contract.

---

# 15. Sensitive-Field Masking

Sensitive-field masking means sensitive internal data is not exposed through the API response.

Common sensitive fields include:

- password
- access token
- refresh token
- secret keys
- internal credentials

Example:

```python
class CreateUserRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
```

Internal object:

```python
{
    "id": 2,
    "username": "uma",
    "password": "Uma@123",
    "role": "user"
}
```

Response:

```json
{
    "id": 2,
    "username": "uma",
    "role": "user"
}
```

The password exists internally but is not part of the public response DTO.

### Important

Response-model masking hides the field from the API response. It does not securely store the password.

Password hashing is a separate security concern.

---

# 16. Complete User DTO Example

```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None

class UserCreateResponse(BaseModel):
    message: str
    user: UserResponse

class LoginResponse(BaseModel):
    message: str
```

The response model intentionally contains no password.

---

# 17. Complete User Creation Endpoint

```python
@router.post(
    "/create/user",
    response_model=UserCreateResponse,
    response_model_exclude_unset=True
)
async def create_user(credentials: create_user):

    user_id = max(user["id"] for user in users) + 1

    new_user = {
        "id": user_id,
        **credentials.model_dump()
    }

    for user in users:
        if user["username"] == credentials.username:
            return {"message": "User already exists"}

    users.append(new_user)

    return {
        "message": "User created successfully",
        "user": new_user
    }
```

Important pieces:

```python
credentials.model_dump()
```

converts the request Pydantic object to dictionary-style data for internal processing.

The returned `new_user` can contain more fields than the public response DTO.

FastAPI serializes it according to `UserCreateResponse` and `UserResponse`.

---

# 18. Login Must Have Its Own Response DTO

Login returns:

```python
{"message": "Login successful"}
```

Therefore:

```python
class LoginResponse(BaseModel):
    message: str
```

Endpoint:

```python
@router.post("/login", response_model=LoginResponse)
async def login(credentials: validate_user):

    for user in users:
        if (
            user["username"] == credentials.username
            and user["password"] == credentials.password
        ):
            return {"message": "Login successful"}

    return {"message": "Invalid username or password"}
```

Do not use:

```python
@router.post("/login", response_model=UserResponse)
```

if login returns only a message.

---

# 19. `ResponseValidationError`

A `ResponseValidationError` occurs when the returned data does not satisfy the declared response model.

Example:

```python
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
```

But:

```python
@router.post("/login", response_model=UserResponse)
async def login(...):
    return {"message": "Login successful"}
```

FastAPI expects:

```text
id
username
role
```

but receives only:

```text
message
```

Therefore it reports missing fields.

The important lesson is:

> The returned data must match the response contract declared by `response_model`.

---

# 20. `response_model_exclude_unset`

Consider:

```python
class UserResponse(BaseModel):
    id: int
    username: str
    role: str = "user"
    email: str | None = None
    phone: str | None = None
    address: str | None = None
```

Here:

- `id` is required.
- `username` is required.
- `role` has a default.
- `email` is optional.
- `phone` is optional.
- `address` is optional.

If only `id` and `username` are explicitly set, then:

```python
response_model_exclude_unset=True
```

can exclude the fields that were not explicitly set.

Conceptually:

```json
{
    "id": 1,
    "username": "venkat"
}
```

This is useful for response models containing optional/default fields.

---

# 21. The Critical Difference: Response Filtering vs `exclude_unset`

These are different.

## Response-model filtering

Question:

> Which fields are allowed in the response at all?

Example:

```python
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
```

If internal data contains:

```text
id
username
password
role
email
phone
address
```

only the fields declared in `UserResponse` form the public response contract.

---

## `response_model_exclude_unset=True`

Question:

> Among the fields declared in the response model, which fields were actually set?

Example:

```python
class UserResponse(BaseModel):
    id: int
    username: str
    role: str = "user"
    email: str | None = None
    phone: str | None = None
```

If only `id` and `username` were explicitly set, `exclude_unset=True` can omit the unset fields.

---

# 22. `exclude_unset` Does Not Mean "Hide Every Undeclared Field"

Suppose:

```python
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
```

and internal data contains:

```python
{
    "id": 1,
    "username": "venkat",
    "password": "secret",
    "email": "venkat@gmail.com"
}
```

You do not need `response_model_exclude_unset=True` to hide password or email.

They are already outside the response model.

The response model itself defines the fields exposed.

---

# 23. `exclude_unset` vs `exclude_none` vs `exclude_defaults`

These options solve different problems.

### `response_model_exclude_unset=True`

Focus:

```text
Was the field explicitly set?
```

Unset → exclude.

### `response_model_exclude_none=True`

Focus:

```text
Is the field's value None?
```

`None` → exclude.

### `response_model_exclude_defaults=True`

Focus:

```text
Does the field equal its declared default?
```

Value equals default → exclude.

Do not treat these options as interchangeable.

---

# 24. Practical User Example

The project used:

```python
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
```

and:

```python
@router.post(
    "/create/user",
    response_model=UserCreateResponse,
    response_model_exclude_unset=True
)
```

Two mechanisms are now demonstrated:

```text
password
    ↓
not declared in UserResponse
    ↓
not exposed
```

and:

```text
email / phone / address
    ↓
declared but optional
    ↓
not explicitly set
    ↓
exclude_unset can omit them
```

This is a useful practical Day 7 example.

---

# 25. Request and Response Architecture

```text
                         CLIENT
                            │
                            │ JSON request
                            ▼
                    ┌──────────────────┐
                    │   Request DTO    │
                    │   Pydantic       │
                    └────────┬─────────┘
                             │
                             │ validated data
                             ▼
                    ┌──────────────────┐
                    │ Router / Service │
                    │ Business Logic   │
                    └────────┬─────────┘
                             │
                             │ internal data
                             ▼
                    ┌──────────────────┐
                    │  Response DTO    │
                    │   Pydantic       │
                    └────────┬─────────┘
                             │
                             │ serialization
                             ▼
                         JSON response
                            │
                            ▼
                          CLIENT
```

---

# 26. User API Architecture

Create user:

```text
Client
  ↓
CreateUserRequest
  ↓
Internal User
  ├── id
  ├── username
  ├── password
  ├── role
  ├── email
  ├── phone
  └── address
  ↓
UserCreateResponse
  ↓
UserResponse
  ├── id
  ├── username
  ├── role
  ├── email if set
  ├── phone if set
  └── address if set
  ↓
Client
```

Password is intentionally absent from the public response DTO.

---

# 27. Login Architecture

```text
Client
  ↓
validate_user
  ↓
Authentication logic
  ├── valid
  │     ↓
  │   LoginResponse
  │     ↓
  │   "Login successful"
  │
  └── invalid
        ↓
      LoginResponse
        ↓
      "Invalid username or password"
```

Both branches have the same response structure.

---

# 28. Common Mistakes Encountered

## Mistake 1 — Wrong response model

Wrong:

```python
@router.post("/login", response_model=UserResponse)
```

when returning:

```python
{"message": "Login successful"}
```

Correct:

```python
@router.post("/login", response_model=LoginResponse)
```

---

## Mistake 2 — Assuming every endpoint uses the same response DTO

Incorrect:

```text
All user endpoints → UserResponse
```

Correct:

```text
Create user → UserCreateResponse
Login       → LoginResponse
Get user    → UserResponse
```

---

## Mistake 3 — Assuming `exclude_unset` hides undeclared fields

Incorrect:

```text
exclude_unset hides password/email/phone/address
```

Correct:

```text
Response DTO controls which fields exist in the public response.

exclude_unset controls declared fields that were not explicitly set.
```

---

## Mistake 4 — Returning different response shapes from different branches

If:

```python
class LoginResponse(BaseModel):
    message: str
```

then both branches should return:

```python
{"message": "..."}
```

Do not return:

```python
{"message": "...", "user": {...}}
```

unless the declared response model supports that structure.

---

# 29. Response Validation vs Request Validation

Request validation:

```text
Client
  ↓
Request DTO
  ↓
Does incoming data match?
```

Response validation:

```text
Endpoint
  ↓
Returned Python object
  ↓
Response DTO
  ↓
Does outgoing data match?
```

Therefore Pydantic participates in both input and output contracts.

---

# 30. Day 7 Professional Mental Model

Think of the API as having two major contracts.

## Input contract

```text
"What will I accept?"
```

Defined by Request DTOs such as:

```text
CreateUserRequest
CreateProductRequest
CreateOrderRequest
```

## Output contract

```text
"What will I expose?"
```

Defined by Response DTOs such as:

```text
UserResponse
ProductResponse
OrderResponse
LoginResponse
```

The internal application object can contain more information than either contract.

That is normal and intentional.

---

# 31. Day 7 Key Rules

1. DTO means Data Transfer Object.
2. DTO is an architectural/data-contract concept, not a special FastAPI class.
3. Pydantic models can implement DTOs.
4. Request DTOs define accepted input.
5. Response DTOs define exposed output.
6. Request and response DTOs do not need to be identical.
7. `response_model` is endpoint-specific.
8. `list[Model]` means a list of that response model.
9. Response DTOs can contain nested DTOs.
10. Response models can filter internal fields.
11. Sensitive fields such as passwords should not be included in public response DTOs.
12. A response model does not replace password hashing or other security mechanisms.
13. `response_model_exclude_unset=True` is about fields not explicitly set.
14. `exclude_unset`, `exclude_none`, and `exclude_defaults` have different meanings.
15. A `ResponseValidationError` means the returned data does not match the declared response contract.
16. Every return path should be compatible with the endpoint's response model.

---

# 32. Day 7 Final Checklist

- [x] DTO meaning
- [x] DTO as an architectural concept
- [x] Pydantic models as DTOs
- [x] Request DTO
- [x] Response DTO
- [x] Request/response separation
- [x] `response_model`
- [x] Response serialization
- [x] Response filtering
- [x] `list[ResponseModel]`
- [x] Nested response models
- [x] Different response DTOs per endpoint
- [x] Sensitive-field masking
- [x] Password exclusion
- [x] Login-specific response DTO
- [x] `ResponseValidationError`
- [x] `response_model_exclude_unset`
- [x] `exclude_unset` vs `exclude_none` vs `exclude_defaults`
- [x] Practical Products example
- [x] Practical Orders example
- [x] Practical Users example
- [x] Debugging response-model mismatches

---

# 33. Final Day 7 Takeaway

The most important mental model is:

```text
REQUEST
"What can the client send?"
        ↓
Request DTO


INTERNAL APPLICATION DATA
"What does the application/service know?"
        ↓
May contain more fields


RESPONSE
"What is the client allowed to receive?"
        ↓
Response DTO
```

A professional API should not automatically expose its entire internal object.

Instead, each endpoint deliberately defines its public data contract.

For example:

```text
Create User
    Request  → username + password + profile data
    Response → message + safe user data

Login
    Request  → username + password
    Response → message

Get User
    Request  → user ID
    Response → safe user data
```

That separation is the core of the **Day 7 DTO Pattern: Request vs Response Schemas**.
