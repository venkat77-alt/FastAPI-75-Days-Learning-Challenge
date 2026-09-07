# 🚀 FastAPI 75-Day Learning Challenge — Day 4

## 📌 Day 4: Pydantic v2 Fundamentals

Today I focused on **Pydantic v2** and how FastAPI uses Pydantic models to validate and structure request data.

Pydantic is one of the core components of FastAPI because it provides:

- Request body validation
- Type checking
- Automatic type conversion
- Default values
- Nested data models
- Strict validation
- API documentation generation through OpenAPI/Swagger

---

## 🎯 What I Learned

### 1. Pydantic `BaseModel`

A Pydantic model is created by inheriting from `BaseModel`.

```python
from pydantic import BaseModel

class CreateProduct(BaseModel):
    item: str
    category: str
    price: int
    stock: int
```

This defines the expected structure of a product request.

FastAPI uses this model to validate incoming JSON data.

---

# 🔗 Connecting Pydantic Schemas with FastAPI Endpoints

A Pydantic schema can be directly used as the request body type of a FastAPI endpoint.

```python
from fastapi import APIRouter
from schemas.schema import CreateProduct

router = APIRouter()

@router.post("/")
async def create_product(product: CreateProduct):
    return {
        "item": product.item,
        "category": product.category,
        "price": product.price,
        "stock": product.stock
    }
```

The important part is:

```python
product: CreateProduct
```

This tells FastAPI that the request body must follow the `CreateProduct` schema.

### Request Example

```json
{
    "item": "iPhone",
    "category": "electronics",
    "price": 50000,
    "stock": 10
}
```

FastAPI receives the JSON and Pydantic validates it before the endpoint function executes.

### Basic Flow

```text
Client
   ↓
JSON Request
   ↓
FastAPI Endpoint
   ↓
Pydantic Validation
   ↓
Validated Data
   ↓
Business Logic
   ↓
Response
```

---

# 🔄 2. Automatic Type Conversion

One useful feature of Pydantic is that it can convert compatible input values into the declared Python types.

For example:

```python
class Product(BaseModel):
    price: int
```

If the input is:

```json
{
    "price": "50000"
}
```

Pydantic may convert the compatible value into:

```python
50000
```

This behavior is useful when working with data coming from external systems.

However, this behavior can be controlled using **strict mode**.

---

# 🎯 3. Strict Mode

Pydantic supports strict validation when exact types are required.

```python
from pydantic import BaseModel, ConfigDict

class CreateProduct(BaseModel):
    model_config = ConfigDict(strict=True)

    item: str
    category: str
    price: int
    stock: int
```

With strict mode enabled:

```json
{
    "item": "iPhone",
    "category": "electronics",
    "price": 50000,
    "stock": 10
}
```

✅ Valid

But:

```json
{
    "item": "iPhone",
    "category": "electronics",
    "price": "50000",
    "stock": "10"
}
```

❌ Validation fails because the values are strings instead of integers.

FastAPI returns a **422 Unprocessable Entity** response when the request doesn't satisfy the schema.

### Important Concept

Normal validation can allow compatible type conversion.

Strict validation requires the input to already have the expected type.

```text
Normal Pydantic
"50000" → 50000
     ↓
Type conversion may happen


Strict Pydantic
"50000" → ❌
     ↓
No automatic conversion
```

---

# 🧩 4. Default Values

Pydantic models can define default values.

```python
class CreateProduct(BaseModel):
    item: str
    category: str
    price: int
    stock: int = 0
```

Now `stock` does not have to be provided.

### Request

```json
{
    "item": "iPhone",
    "category": "electronics",
    "price": 50000
}
```

Pydantic uses:

```python
stock = 0
```

So the validated model contains:

```python
{
    "item": "iPhone",
    "category": "electronics",
    "price": 50000,
    "stock": 0
}
```

### Important Difference

This:

```python
stock: int
```

means the field is required.

This:

```python
stock: int = 0
```

means the field is optional during input and defaults to `0` when omitted.

---

# 📝 5. Field Descriptions

Pydantic's `Field()` can be used to add metadata and descriptions.

```python
from pydantic import BaseModel, Field

class CreateProduct(BaseModel):
    item: str = Field(description="Name of the product")
    category: str = Field(description="Product category")
    price: int = Field(description="Product price")
    stock: int = Field(default=0, description="Available stock")
```

These descriptions can appear automatically in FastAPI's Swagger/OpenAPI documentation.

This makes the API easier for other developers to understand.

---

# 🏗️ 6. Nested Pydantic Schemas

Pydantic models can contain other Pydantic models.

For example:

```python
from pydantic import BaseModel

class Supplier(BaseModel):
    name: str
    contact: str

class CreateProduct(BaseModel):
    item: str
    category: str
    price: int
    stock: int = 0
    supplier: Supplier
```

The request can then look like:

```json
{
    "item": "iPhone",
    "category": "electronics",
    "price": 50000,
    "stock": 10,
    "supplier": {
        "name": "ABC Electronics",
        "contact": "9876543210"
    }
}
```

Pydantic validates both the product data and the nested supplier data.

---

# 📁 Project Structure

The Day 4 project was organized as:

```text
day_4/
│
├── main.py
├── products.py
├── orders.py
│
└── schemas/
    └── schema.py
```

The schemas are separated from the API endpoint files so that request models can be maintained independently.

---

# 📦 Product Schemas

Example:

```python
from pydantic import BaseModel

class CreateProduct(BaseModel):
    item: str
    category: str
    price: int
    stock: int = 0

class UpdateProduct(BaseModel):
    item: str
    category: str
    price: int
    stock: int
```

These models can then be imported into the product router.

```python
from schemas.schema import CreateProduct
```

And used in the endpoint:

```python
@router.post("/")
async def create_product(product: CreateProduct):
    new_product = {
        "item": product.item,
        "category": product.category,
        "price": product.price,
        "stock": product.stock
    }

    return new_product
```

---

# 🛒 Order Schemas

Example:

```python
from pydantic import BaseModel

class CreateOrder(BaseModel):
    item: str
    quantity: int

class UpdateOrder(BaseModel):
    item: str
    quantity: int
```

Used in the endpoint:

```python
@router.post("/")
async def create_order(order: CreateOrder):
    return {
        "item": order.item,
        "quantity": order.quantity
    }
```

---

# ❌ Validation Errors and HTTP 422

When incoming data doesn't match the Pydantic schema, FastAPI automatically returns a validation error.

For example, if:

```python
class CreateProduct(BaseModel):
    item: str
    price: int
```

and the client sends:

```json
{
    "item": "iPhone",
    "price": "invalid"
}
```

the request fails validation.

FastAPI returns:

```text
422 Unprocessable Entity
```

This happens **before the endpoint's main logic is executed**.

---

# 🧠 Important Day 4 Mental Model

Pydantic is responsible for defining and validating the shape of data.

```text
                 PYDANTIC
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
       Types      Defaults   Validation
          │          │          │
          └──────────┼──────────┘
                     ↓
              FastAPI Endpoint
```

A FastAPI endpoint can therefore receive structured, validated Python objects instead of manually processing raw JSON.

---

# 🔥 Day 4 Key Takeaways

### `BaseModel`

Used to create Pydantic data models.

```python
class Product(BaseModel):
    name: str
    price: int
```

### Type Conversion

Pydantic can convert compatible input values depending on the validation configuration.

### Strict Mode

Use:

```python
ConfigDict(strict=True)
```

when exact input types are required.

### Default Values

Use:

```python
stock: int = 0
```

when a field should receive a default value if it isn't provided.

### Field Descriptions

Use:

```python
Field(description="...")
```

to provide useful API documentation metadata.

### Nested Schemas

Pydantic models can contain other Pydantic models.

### FastAPI Integration

A schema can be directly used as an endpoint request body:

```python
async def create_product(product: CreateProduct):
```

---

# 🧪 Day 4 Testing Checklist

I tested the Pydantic schemas through FastAPI/Swagger with scenarios such as:

- ✅ Valid product request
- ✅ Valid order request
- ✅ Missing required field
- ✅ Invalid field type
- ✅ Automatic type conversion
- ✅ Default value behavior
- ✅ Strict type validation
- ✅ Nested Pydantic schema
- ✅ Pydantic schema integrated with FastAPI endpoints
- ✅ Validation errors returning HTTP 422

---

# 🏆 Day 4 Completed

Day 4 strengthened the understanding of how **FastAPI and Pydantic work together to create validated and structured APIs**.

The key concept learned today:

```text
JSON Request
     ↓
Pydantic Schema
     ↓
Validation / Conversion
     ↓
Python Object
     ↓
FastAPI Endpoint
     ↓
Application Logic
```

## 🚀 Next: Day 5

**Advanced Pydantic v2**

Upcoming concepts:

- Custom validators
- Model validation
- Custom serialization
- Advanced data validation

---

### 📚 Technologies Used

- Python
- FastAPI
- Pydantic v2
- Uvicorn
- Swagger / OpenAPI