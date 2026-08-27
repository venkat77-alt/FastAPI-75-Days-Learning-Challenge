# FastAPI Day 2 — Routing, Path Parameters & Query Parameters

> **Day 2 focus:** Route Controllers, RESTful URL design, Path Parameters, Query Parameters, optional/default parameters, and parameter validation with `Path()` and `Query()`.
>
> **Important:** Pydantic / response validation is **not included in these Day 2 notes**.

---

## 1. Day 2 Learning Goals

By the end of Day 2, you should understand:

- Route controllers with `APIRouter`
- `include_router()`
- URL prefixes and tags
- RESTful URL structure
- Path parameters
- Python type hints
- Query parameters
- Optional query parameters
- Default values
- Multiple query parameters
- Search and filtering
- `Path()` validation
- `Query()` validation

---

# 2. Route Controllers

A route controller is the part of the API that receives a request and maps it to a Python function.

Example:

```python
@router.get("/")
async def get_products():
    return products
```

The route:

```text
GET /
```

is connected to:

```python
get_products()
```

When the router is included in `main.py` with:

```python
app.include_router(
    product_router,
    prefix="/products",
    tags=["products"]
)
```

the final URL becomes:

```text
GET /products/
```

---

# 3. Why Use `APIRouter()`?

Instead of putting every endpoint in `main.py`, routes can be separated by feature.

Example project:

```text
day_2/
│
├── main.py
├── products.py
└── orders.py
```

### `products.py`

Contains product-related routes.

### `orders.py`

Contains order-related routes.

### `main.py`

Creates the FastAPI application and connects the routers.

This makes the project easier to organize as it grows.

---

# 4. `main.py` Example

```python
from fastapi import FastAPI

from products import router as product_router
from orders import router as order_router


app = FastAPI(
    title="Day 2 E-Commerce API",
    description="Routing, path parameters and query parameters"
)


app.include_router(
    product_router,
    prefix="/products",
    tags=["products"]
)


app.include_router(
    order_router,
    prefix="/orders",
    tags=["orders"]
)
```

---

# 5. Understanding `include_router()`

Suppose `products.py` contains:

```python
@router.get("/")
async def get_products():
    return products
```

And `main.py` contains:

```python
app.include_router(
    product_router,
    prefix="/products"
)
```

FastAPI combines them:

```text
/products + /
     ↓
/products/
```

Similarly:

```python
@router.get("/{id}")
async def get_product(id: int):
    ...
```

becomes:

```text
/products/{id}
```

A request such as:

```text
GET /products/5
```

can therefore call:

```python
get_product(id=5)
```

---

# 6. Path Parameters

A **path parameter** is a value contained directly inside the URL path.

Example:

```text
/products/5
```

Here:

```text
5
```

is the path parameter.

The route is:

```python
@router.get("/{id}")
async def get_product(id: int):
    ...
```

The `{id}` tells FastAPI to capture that part of the URL.

---

# 7. Why Path Parameters Are Needed

Imagine an e-commerce database containing thousands of products.

This request:

```text
GET /products/
```

means:

> Give me the product collection.

But:

```text
GET /products/5
```

means:

> Give me the product identified by ID 5.

Therefore:

```text
/products/
```

is the collection.

```text
/products/5
```

identifies one specific resource.

### Simple rule

> **Path parameter = Which specific resource?**

---

# 8. Path Parameter Example

```python
from fastapi import APIRouter

router = APIRouter()


products = [
    {
        "id": 1,
        "item": "mobile",
        "category": "electronics",
        "price": 10000,
        "stock": 20
    },
    {
        "id": 2,
        "item": "laptop",
        "category": "electronics",
        "price": 50000,
        "stock": 10
    }
]


@router.get("/{id}")
async def get_product(id: int):

    for product in products:

        if product["id"] == id:
            return product

    return {
        "message": "product not found"
    }
```

---

# 9. Understanding the Path Parameter Code

Request:

```text
GET /products/2
```

FastAPI extracts:

```python
id = 2
```

Then calls:

```python
get_product(id=2)
```

The loop checks:

```python
for product in products:
```

Each product is examined.

Then:

```python
if product["id"] == id:
```

checks whether the current product has the requested ID.

If it does:

```python
return product
```

returns that product.

---

# 10. Type Hints

A Python **type hint** tells Python/FastAPI what type of value a parameter is expected to contain.

Example:

```python
id: int
```

Here:

```text
id
↓
parameter name

int
↓
type hint
```

Another example:

```python
search: str
```

means `search` is expected to be a string.

---

# 11. Why Type Hints Matter in FastAPI

Consider:

```python
@router.get("/{id}")
async def get_product(id: int):
    ...
```

The type hint:

```python
int
```

tells FastAPI that `id` should be an integer.

Valid example:

```text
/products/5
```

Invalid example:

```text
/products/abc
```

FastAPI can detect that `"abc"` cannot be interpreted as an integer and return a validation error.

---

# 12. Path Parameter Validation With `Path()`

`Path()` is a FastAPI utility used to add validation and metadata to a path parameter.

Example:

```python
from fastapi import Path


@router.get("/{id}")
async def get_product(
    id: int = Path(..., gt=0)
):
    ...
```

There are three important parts:

```python
id: int = Path(..., gt=0)
│   │      │
│   │      └── FastAPI Path configuration/validation
│   │
│   └── Python type hint
│
└── parameter name
```

---

# 13. `id: int` vs `Path()`

These are different concepts.

```python
id: int
```

is the **type hint**.

It says:

> `id` should be an integer.

```python
Path(..., gt=0)
```

is **FastAPI validation/configuration**.

It says:

> The path parameter is required and must be greater than 0.

Therefore:

```python
id: int = Path(..., gt=0)
```

means:

```text
id
↓
must be an integer
↓
must be greater than 0
```

---

# 14. Understanding `...` in `Path()`

Example:

```python
Path(...)
```

The:

```python
...
```

indicates that there is no default value and the parameter is required.

For a path parameter, this is natural because the URL itself contains the required value.

For example:

```text
/products/{id}
```

requires an ID.

---

# 15. `gt` — Greater Than

```python
id: int = Path(..., gt=0)
```

means:

```text
id > 0
```

Examples:

```text
/products/1      ✅
/products/5      ✅
/products/100    ✅

/products/0      ❌
/products/-5     ❌
```

---

# 16. Other Path Validation Rules

## `gt`

Greater than:

```python
id: int = Path(..., gt=0)
```

Means:

```text
id > 0
```

---

## `ge`

Greater than or equal to:

```python
id: int = Path(..., ge=1)
```

Means:

```text
id >= 1
```

---

## `lt`

Less than:

```python
id: int = Path(..., lt=100)
```

Means:

```text
id < 100
```

---

## `le`

Less than or equal to:

```python
id: int = Path(..., le=100)
```

Means:

```text
id <= 100
```

---

# 17. Complete Path Parameter Example With Validation

```python
from fastapi import APIRouter, Path

router = APIRouter()


@router.get("/{id}")
async def get_product(
    id: int = Path(..., gt=0)
):

    for product in products:

        if product["id"] == id:
            return product

    return {
        "message": "product not found"
    }
```

For:

```text
GET /products/5
```

the approximate flow is:

```text
/products/5
     ↓
Extract 5
     ↓
Convert/check as int
     ↓
Check gt=0
     ↓
5 > 0 ✅
     ↓
get_product(id=5)
```

---

# 18. Query Parameters

A **query parameter** is a value placed after `?` in the URL.

Example:

```text
/products/?search=mobile
```

Here:

```text
search=mobile
```

is the query parameter.

General structure:

```text
/path?parameter=value
```

---

# 19. Why Query Parameters Are Needed

In an e-commerce application, users may want to:

- Search products
- Filter by category
- Filter by minimum price
- Filter by maximum price
- Combine multiple filters

Instead of creating a new path for every possible filter, query parameters allow the client to send filtering instructions.

Examples:

```text
/products/?search=mobile
```

```text
/products/?category=electronics
```

```text
/products/?min_price=10000
```

```text
/products/?max_price=30000
```

### Simple rule

> **Query parameter = How should I search/filter the collection?**

---

# 20. Path Parameter vs Query Parameter

## Path Parameter

```text
/products/5
```

Used to identify a specific resource.

```text
5
↑
product ID
```

## Query Parameter

```text
/products/?search=mobile
```

Used to search or filter a collection.

```text
search=mobile
↑
filter/search instruction
```

### Remember

```text
Path Parameter
→ Which resource?

Query Parameter
→ How should the collection be filtered/searched?
```

---

# 21. Basic Query Parameter

Example:

```python
@router.get("/")
async def get_products(
    search: str | None = None
):
    ...
```

Here:

```python
search
```

is a query parameter.

Why?

Because it is a function parameter that is not part of the path:

```text
/products/?search=mobile
```

FastAPI reads `search` from the query string.

---

# 22. Understanding `str | None = None`

Consider:

```python
search: str | None = None
```

Break it down:

```text
search
↓
parameter name

str
↓
expected type

|
↓
OR

None
↓
parameter may be absent

= None
↓
default value
```

Therefore:

```text
/products/
```

results in:

```python
search = None
```

while:

```text
/products/?search=mobile
```

results in:

```python
search = "mobile"
```

---

# 23. Query Parameters Are Not Type Hints

This is extremely important.

Consider:

```python
search: str | None = Query(
    None,
    min_length=2
)
```

The type hint is:

```python
str | None
```

`Query()` is **not** the type hint.

It is a FastAPI utility for configuring and validating the query parameter.

Think of it as:

```python
parameter_name: TYPE_HINT = FASTAPI_CONFIGURATION(...)
```

Example:

```python
search: str | None = Query(None, min_length=2)
```

```text
search
  ↓
parameter name

str | None
  ↓
type hint

Query(...)
  ↓
FastAPI configuration/validation
```

---

# 24. Query Parameter With `Query()`

Import:

```python
from fastapi import Query
```

Then:

```python
search: str | None = Query(
    None,
    min_length=2
)
```

This means:

- `search` is a string or `None`
- default value is `None`
- if supplied, it must have at least 2 characters

---

# 25. Search Filter

Example:

```python
if search is not None:

    if search.lower() not in product["item"].lower():
        continue
```

Suppose:

```python
product["item"] = "laptop"
```

and:

```python
search = "lap"
```

Python checks:

```python
"lap" in "laptop"
```

The result is:

```text
True
```

So the product remains in the result.

This allows partial search.

Examples:

```text
search=lap
```

can match:

```text
laptop
```

and:

```text
search=top
```

can also match:

```text
laptop
```

---

# 26. Case-Insensitive Search

We use:

```python
search.lower()
```

and:

```python
product["item"].lower()
```

Therefore these can match the same product:

```text
mobile
Mobile
MOBILE
mObIlE
```

This makes the search case-insensitive.

---

# 27. Category Filter

Example:

```python
if category is not None:

    if product["category"].lower() != category.lower():
        continue
```

Request:

```text
/products/?category=electronics
```

FastAPI gives:

```python
category = "electronics"
```

The code performs an exact category comparison while ignoring capitalization.

For example:

```text
electronics
Electronics
ELECTRONICS
```

can match:

```text
electronics
```

But:

```text
electronic
```

does not match:

```text
electronics
```

because it is a different string.

---

# 28. Minimum Price Filter

Example:

```python
if min_price is not None:

    if product["price"] < min_price:
        continue
```

Request:

```text
/products/?min_price=20000
```

The meaning is:

> Return products whose price is at least 20,000.

Example:

```text
Product price = 15000
Minimum price = 20000
```

Check:

```python
15000 < 20000
```

Result:

```text
True
```

So that product is skipped.

---

# 29. Maximum Price Filter

Example:

```python
if max_price is not None:

    if product["price"] > max_price:
        continue
```

Request:

```text
/products/?max_price=10000
```

The meaning is:

> Return products whose price is no greater than 10,000.

Example:

```text
Product price = 12000
Maximum price = 10000
```

Check:

```python
12000 > 10000
```

Result:

```text
True
```

So the product is skipped.

---

# 30. Multiple Query Parameters

Multiple query parameters are separated using:

```text
&
```

Example:

```text
/products/?category=electronics&max_price=30000
```

FastAPI receives:

```python
category = "electronics"
max_price = 30000
```

The product must satisfy both conditions.

---

# 31. Four Query Parameters

Our e-commerce endpoint can use:

```python
search: str | None = None
category: str | None = None
min_price: int | None = None
max_price: int | None = None
```

This allows requests such as:

```text
/products/?search=mobile
```

```text
/products/?category=electronics
```

```text
/products/?min_price=10000
```

```text
/products/?max_price=30000
```

and combinations such as:

```text
/products/?search=mobile&category=electronics&min_price=10000&max_price=15000
```

---

# 32. Current Practice Data

```python
products = [
    {
        "id": 1,
        "item": "mobile",
        "category": "electronics",
        "price": 10000,
        "stock": 20
    },
    {
        "id": 2,
        "item": "mobile",
        "category": "electronics",
        "price": 12000,
        "stock": 15
    },
    {
        "id": 3,
        "item": "mobile",
        "category": "electronics",
        "price": 15000,
        "stock": 8
    },
    {
        "id": 4,
        "item": "laptop",
        "category": "electronics",
        "price": 50000,
        "stock": 10
    },
    {
        "id": 5,
        "item": "laptop",
        "category": "electronics",
        "price": 55000,
        "stock": 7
    },
    {
        "id": 6,
        "item": "laptop",
        "category": "electronics",
        "price": 65000,
        "stock": 5
    },
    {
        "id": 7,
        "item": "tablet",
        "category": "electronics",
        "price": 20000,
        "stock": 15
    },
    {
        "id": 8,
        "item": "tablet",
        "category": "electronics",
        "price": 25000,
        "stock": 10
    },
    {
        "id": 9,
        "item": "tablet",
        "category": "electronics",
        "price": 30000,
        "stock": 6
    },
    {
        "id": 10,
        "item": "headphones",
        "category": "audio",
        "price": 3000,
        "stock": 30
    },
    {
        "id": 11,
        "item": "headphones",
        "category": "audio",
        "price": 5000,
        "stock": 20
    },
    {
        "id": 12,
        "item": "headphones",
        "category": "audio",
        "price": 8000,
        "stock": 12
    },
    {
        "id": 13,
        "item": "keyboard",
        "category": "computer_accessories",
        "price": 2500,
        "stock": 25
    },
    {
        "id": 14,
        "item": "keyboard",
        "category": "computer_accessories",
        "price": 3500,
        "stock": 18
    },
    {
        "id": 15,
        "item": "mouse",
        "category": "computer_accessories",
        "price": 1500,
        "stock": 40
    },
    {
        "id": 16,
        "item": "mouse",
        "category": "computer_accessories",
        "price": 2500,
        "stock": 25
    },
    {
        "id": 17,
        "item": "monitor",
        "category": "computer_accessories",
        "price": 15000,
        "stock": 12
    },
    {
        "id": 18,
        "item": "monitor",
        "category": "computer_accessories",
        "price": 22000,
        "stock": 8
    },
    {
        "id": 19,
        "item": "smartwatch",
        "category": "wearables",
        "price": 8000,
        "stock": 18
    },
    {
        "id": 20,
        "item": "smartwatch",
        "category": "wearables",
        "price": 12000,
        "stock": 10
    }
]
```

---

# 33. Complete GET Products Query Filter

```python
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_products(
    search: str | None = None,
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None
):

    filtered_product = []

    for product in products:

        if search is not None:

            if search.lower() not in product["item"].lower():
                continue

        if category is not None:

            if product["category"].lower() != category.lower():
                continue

        if min_price is not None:

            if product["price"] < min_price:
                continue

        if max_price is not None:

            if product["price"] > max_price:
                continue

        filtered_product.append(product)

    return filtered_product
```

---

# 34. Why `filtered_product` Is Needed

We create:

```python
filtered_product = []
```

This is the list that will contain products that pass all filters.

Then:

```python
for product in products:
```

checks every product.

If the product passes all filters:

```python
filtered_product.append(product)
```

adds it to the result.

Finally:

```python
return filtered_product
```

returns every matching product.

---

# 35. Important Difference: `product` vs `filtered_product`

Inside:

```python
for product in products:
```

`product` represents **one product at a time**.

For example:

```text
product → mobile
product → laptop
product → tablet
```

But:

```python
filtered_product
```

is a list containing **all products that passed the filters**.

Therefore:

```python
return product
```

returns only one product.

Correct:

```python
return filtered_product
```

returns all matching products.

---

# 36. Why `continue` Is Used

Example:

```python
if product["price"] > max_price:
    continue
```

`continue` means:

> Skip the current product and move to the next product in the loop.

Example:

```text
Product 1
   ↓
passes filters
   ↓
append


Product 2
   ↓
fails filter
   ↓
continue
   ↓
skip


Product 3
   ↓
passes filters
   ↓
append
```

---

# 37. Multiple Filters Behave Like AND

Suppose the request is:

```text
/products/?category=electronics&min_price=10000&max_price=30000
```

The product must satisfy:

```text
category = electronics
AND
price >= 10000
AND
price <= 30000
```

If any condition fails, the product is skipped.

---

# 38. No Filters

Request:

```text
GET /products/
```

All query parameters are:

```python
search = None
category = None
min_price = None
max_price = None
```

No filter is applied.

Therefore all products are returned.

---

# 39. No Matching Products

Suppose:

```text
GET /products/?min_price=100000
```

and no product has a price of ₹100,000 or more.

Then:

```python
filtered_product
```

remains:

```python
[]
```

The API returns:

```json
[]
```

This means:

> The request was valid, but no products matched the filters.

---

# 40. Query Validation With `Query()`

Import:

```python
from fastapi import Query
```

Example:

```python
search: str | None = Query(
    None,
    min_length=2
)
```

This adds validation.

If `search` is supplied, it must contain at least 2 characters.

---

# 41. `min_length`

Example:

```python
search: str | None = Query(
    None,
    min_length=2
)
```

Valid:

```text
/products/?search=lap
```

Invalid:

```text
/products/?search=l
```

because `"l"` contains only one character.

---

# 42. Numeric Query Validation

Example:

```python
min_price: int | None = Query(
    None,
    ge=0
)
```

`ge` means:

```text
greater than or equal to
```

Therefore:

```text
min_price=0       ✅
min_price=10000   ✅
min_price=-500    ❌
```

---

# 43. Other Query Validation Rules

## `gt`

Greater than:

```python
min_price: int | None = Query(
    None,
    gt=0
)
```

Means:

```text
min_price > 0
```

---

## `ge`

Greater than or equal to:

```python
min_price: int | None = Query(
    None,
    ge=0
)
```

Means:

```text
min_price >= 0
```

---

## `lt`

Less than:

```python
max_price: int | None = Query(
    None,
    lt=100000
)
```

Means:

```text
max_price < 100000
```

---

## `le`

Less than or equal to:

```python
max_price: int | None = Query(
    None,
    le=100000
)
```

Means:

```text
max_price <= 100000
```

---

# 44. Complete Query Validation Example

```python
from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/")
async def get_products(
    search: str | None = Query(
        None,
        min_length=2
    ),

    category: str | None = Query(
        None,
        min_length=3
    ),

    min_price: int | None = Query(
        None,
        ge=0
    ),

    max_price: int | None = Query(
        None,
        ge=0
    )
):

    filtered_product = []

    for product in products:

        if search is not None:

            if search.lower() not in product["item"].lower():
                continue

        if category is not None:

            if product["category"].lower() != category.lower():
                continue

        if min_price is not None:

            if product["price"] < min_price:
                continue

        if max_price is not None:

            if product["price"] > max_price:
                continue

        filtered_product.append(product)

    return filtered_product
```

---

# 45. Complete Path + Query Validation Example

```python
from fastapi import APIRouter, Path, Query

router = APIRouter()


@router.get("/")
async def get_products(
    search: str | None = Query(
        None,
        min_length=2
    ),

    category: str | None = Query(
        None,
        min_length=3
    ),

    min_price: int | None = Query(
        None,
        ge=0
    ),

    max_price: int | None = Query(
        None,
        ge=0
    )
):

    filtered_product = []

    for product in products:

        if search is not None:

            if search.lower() not in product["item"].lower():
                continue

        if category is not None:

            if product["category"].lower() != category.lower():
                continue

        if min_price is not None:

            if product["price"] < min_price:
                continue

        if max_price is not None:

            if product["price"] > max_price:
                continue

        filtered_product.append(product)

    return filtered_product


@router.get("/{id}")
async def get_product(
    id: int = Path(..., gt=0)
):

    for product in products:

        if product["id"] == id:
            return product

    return {
        "message": "product not found"
    }
```

---

# 46. Path + Query Parameter Together

An endpoint can contain both path and query parameters.

Example request:

```text
GET /products/5?currency=INR
```

Here:

```text
/products/5
          ↑
     path parameter


?currency=INR
 ↑
query parameter
```

Example:

```python
from fastapi import Path, Query


@router.get("/{id}")
async def get_product(
    id: int = Path(..., gt=0),
    currency: str | None = Query(None)
):

    for product in products:

        if product["id"] == id:
            return product

    return {
        "message": "product not found"
    }
```

---

# 47. Common Query Parameter Practice Requests

### Get all products

```text
GET /products/
```

### Search mobile

```text
GET /products/?search=mobile
```

### Partial search

```text
GET /products/?search=lap
```

### Filter by category

```text
GET /products/?category=electronics
```

### Minimum price

```text
GET /products/?min_price=20000
```

### Maximum price

```text
GET /products/?max_price=10000
```

### Category + minimum price

```text
GET /products/?category=electronics&min_price=10000
```

### Category + maximum price

```text
GET /products/?category=electronics&max_price=30000
```

### Price range

```text
GET /products/?min_price=10000&max_price=30000
```

### Search + category

```text
GET /products/?search=mobile&category=electronics
```

### Search + category + price range

```text
GET /products/?search=mobile&category=electronics&min_price=10000&max_price=15000
```

### Product by ID

```text
GET /products/5
```

---

# 48. Type Hint vs `Path()` vs `Query()`

This is the most important distinction to remember.

## Example 1

```python
id: int = Path(..., gt=0)
```

```text
id
↓
parameter name

int
↓
Python type hint

Path(...)
↓
FastAPI path configuration

gt=0
↓
validation rule
```

---

## Example 2

```python
search: str | None = Query(
    None,
    min_length=2
)
```

```text
search
↓
parameter name

str | None
↓
Python type hint

Query(...)
↓
FastAPI query configuration

min_length=2
↓
validation rule
```

### General pattern

```python
name: TYPE_HINT = FASTAPI_CONFIGURATION(...)
```

Examples:

```python
id: int = Path(..., gt=0)

search: str | None = Query(None, min_length=2)

min_price: int | None = Query(None, ge=0)
```

---

# 49. Day 2 Mental Model

```text
ROUTING
    ↓
Which Python function handles the request?


PATH PARAMETER
    ↓
Which specific resource?
    ↓
/products/5


QUERY PARAMETER
    ↓
How should I search/filter the collection?
    ↓
/products/?search=mobile


MULTIPLE QUERY PARAMETERS
    ↓
Combine filters
    ↓
/products/?category=electronics&min_price=10000&max_price=30000


TYPE HINT
    ↓
What type of data is expected?
    ↓
int
str
str | None
int | None


Path() / Query()
    ↓
FastAPI configuration + validation
```

---

# 50. Day 2 Final Checklist

## Routing

- [x] `APIRouter()`
- [x] Route controllers
- [x] `include_router()`
- [x] Prefixes
- [x] Tags
- [x] RESTful URL structure
- [x] GET routes

## Path Parameters

- [x] What path parameters are
- [x] `{id}`
- [x] Type hints
- [x] Retrieve a product by ID
- [x] `Path()`
- [x] `gt`
- [x] `ge`
- [x] `lt`
- [x] `le`

## Query Parameters

- [x] What query parameters are
- [x] `?`
- [x] `&`
- [x] Optional parameters
- [x] Default values
- [x] Search
- [x] Partial search
- [x] Case-insensitive search
- [x] Category filtering
- [x] Minimum price
- [x] Maximum price
- [x] Multiple query parameters
- [x] `continue`
- [x] `filtered_product`
- [x] `Query()`
- [x] Query validation

---

# 51. What NOT to Study Yet

Do not mix the following into Day 2:

```text
Pydantic BaseModel
Request body models
Response models
Custom Pydantic validators
field_validator
model_validator
model_dump()
DTOs
Database models
SQLAlchemy
Authentication
JWT
```

These belong to later stages of the roadmap.

For Day 2, focus on:

```text
Routing
    ↓
Path Parameters
    ↓
Query Parameters
    ↓
Multiple Filters
    ↓
Path()
    ↓
Query()
    ↓
Parameter Validation
```

---

# 52. Final Summary

### Route Controller

Connects an HTTP request to a Python function.

```python
@router.get("/")
async def get_products():
    ...
```

### Path Parameter

Identifies a specific resource.

```text
/products/5
```

```python
id: int
```

### Query Parameter

Controls searching/filtering.

```text
/products/?search=mobile
```

```python
search: str | None = None
```

### Multiple Query Parameters

```text
/products/?category=electronics&min_price=10000&max_price=30000
```

### Type Hint

Defines the expected Python data type.

```python
id: int
search: str | None
min_price: int | None
```

### `Path()`

Adds FastAPI configuration/validation to path parameters.

```python
id: int = Path(..., gt=0)
```

### `Query()`

Adds FastAPI configuration/validation to query parameters.

```python
search: str | None = Query(None, min_length=2)
```

### Most Important Rule

```text
Type hint
→ What type of data?

Path() / Query()
→ FastAPI parameter configuration and validation
```

---

## Day 2 Complete

At this point, you should be comfortable reading and writing:

```python
@router.get("/{id}")
async def get_product(
    id: int = Path(..., gt=0)
):
    ...


@router.get("/")
async def get_products(
    search: str | None = Query(None, min_length=2),
    category: str | None = Query(None, min_length=3),
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0)
):
    ...
```

The next roadmap topics should be studied only after you are comfortable with these Day 2 concepts.
