# Day 5 — Advanced Pydantic v2
## FastAPI 75-Day Learning Challenge

### Topics Covered
1. `@field_validator`
2. `@model_validator`
3. Regex validation
4. `model_dump()`
5. `model_dump_json()`
6. `include`
7. `exclude`
8. `exclude_none`
9. `exclude_unset`

---

## 1. Why Day 5?

Basic Pydantic types such as:

```python
username: str
price: int
```

only provide basic type validation.

Real backend applications need additional rules:

- usernames must follow a format
- passwords must satisfy security-related format rules
- prices cannot be negative
- discount price cannot exceed original price
- strings may need trimming/normalization
- validated models sometimes need conversion into dictionaries or JSON

Day 5 teaches how to implement these rules cleanly.

---

# 2. `@field_validator`

## What is it?

`@field_validator` is used for custom validation of one or more individual fields.

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Please enter a valid username.")

        return value
```

## Why?

Pydantic knows that `username` must be a string, but it does not automatically know your custom business rule.

For example:

```text
"     "
```

is technically a string, but it is not a meaningful username.

The validator lets us implement that rule.

## Project example

We used this in `createproduct`:

```python
@field_validator("item")
@classmethod
def validate_item(cls, value):
    value = value.strip()

    if not value:
        raise ValueError("Please enter a valid item name.")

    if len(value) < 3:
        raise ValueError("Item name must be at least 3 characters long.")

    return value
```

Request:

```json
{
    "item": "   Laptop   "
}
```

After validation:

```text
"Laptop"
```

The validator both validates and normalizes the value.

---

# 3. Validating Multiple Fields

A single field validator can be applied to multiple fields:

```python
@field_validator("price", "stock")
@classmethod
def validate_price_and_stock(cls, value):
    if value < 0:
        raise ValueError("Price and stock cannot be negative.")

    return value
```

This avoids repeating the same validation code.

---

# 4. `Field()` vs `@field_validator`

Use `Field()` for simple constraints:

```python
username: str = Field(
    min_length=3,
    max_length=20
)
```

Use `@field_validator` when custom Python logic is needed:

```python
@field_validator("username")
@classmethod
def validate_username(cls, value):
    value = value.strip()

    if not value:
        raise ValueError("Username cannot be empty.")

    return value
```

### Mental model

```text
Simple constraint
        ↓
     Field()

Custom field logic
        ↓
@field_validator
```

---

# 5. `@model_validator`

## What is it?

`@model_validator` is used when validation depends on multiple fields together.

Our product example:

```python
@model_validator(mode="after")
def validate_discount_against_price(self):
    if self.Discount_price > self.price:
        raise ValueError(
            "Discount price cannot be greater than the original price."
        )

    return self
```

## Why?

Consider:

```text
price = 50000
Discount_price = 60000
```

Both values are valid integers.

But together they violate the business rule:

```text
Discount_price <= price
```

That is a relationship between two fields, so model-level validation is appropriate.

### Mental model

```text
field_validator
    ↓
"Is this field valid?"

model_validator
    ↓
"Do these fields make sense together?"
```

---

# 6. `mode="after"`

Our validator uses:

```python
@model_validator(mode="after")
```

The model's fields have already been validated, so we can work with:

```python
self.price
self.Discount_price
```

Example:

```python
@model_validator(mode="after")
def validate_discount_against_price(self):
    if self.Discount_price > self.price:
        raise ValueError("Invalid discount.")

    return self
```

---

# 7. Validator Naming Mistake We Fixed

Initially, the field validator and model validator had the same method name:

```python
validate_discount_price
```

We changed the model validator to:

```python
validate_discount_against_price
```

### Lesson

Give validators meaningful and unique method names.

---

# 8. Regex Validation

## What is Regex?

Regex (regular expression) is a pattern used to describe the allowed structure of text.

Example username:

```python
r"^[A-Za-z][A-Za-z0-9_]*$"
```

This means:

- first character must be a letter
- later characters may be letters
- numbers are allowed
- underscore is allowed
- spaces and other special characters are not allowed

Examples:

```text
Uma123       → valid
Uma_Reddy    → valid
uma_123      → valid

123Uma       → invalid
Uma Reddy    → invalid
Uma@123      → invalid
```

---

# 9. Password Regex

We discussed:

```python
r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$"
```

This requires:

- at least one letter
- at least one digit
- minimum 6 characters
- only letters and digits

Examples:

```text
Uma123       → valid
password1    → valid

password     → invalid
123456       → invalid
Uma12        → invalid
```

## Using it with Python `re`

```python
import re

@field_validator("password")
@classmethod
def validate_password(cls, value):
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$"

    if not re.fullmatch(pattern, value):
        raise ValueError(
            "Password must contain at least one letter and one digit."
        )

    return value
```

---

# 10. Pydantic v2 Regex Limitation

Pydantic v2 uses a Rust-based regex engine for `Field(pattern=...)`.

Look-around such as:

```text
(?=...)
```

is not supported by that engine.

Therefore, when we specifically need a lookahead regex such as:

```python
r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$"
```

we can use Python's `re` module inside a `@field_validator`.

---

# 11. Real-World Regex Examples

### Indian phone number

```python
r"^[6-9][0-9]{9}$"
```

### Indian PIN code

```python
r"^[0-9]{6}$"
```

### Product code

```python
r"^[A-Z]{3,5}-[0-9]{4}$"
```

### Employee ID

```python
r"^EMP-[0-9]{4}-[0-9]{3}$"
```

### Insurance policy

```python
r"^POL-[0-9]{4}-[A-Z]{3}[0-9]{5}$"
```

### API version

```python
r"^v[0-9]+$"
```

---

# 12. When NOT to Use Regex

Regex is mainly for string-format validation.

Do not use Regex for:

### Numeric business rules

Use Python logic:

```python
if price <= 0:
    ...
```

### Cross-field relationships

Use:

```python
@model_validator
```

for:

```text
discount <= price
```

### Database existence

Regex cannot answer:

```text
Does this username already exist?
```

That belongs to service/database logic.

### Dates

When the value represents a real date, use appropriate date types and validation instead of unnecessarily treating it as a string.

---

# 13. Validation Decision Architecture

```text
Basic constraint?
       ↓
   Field()

String format?
       ↓
    Regex

Custom rule for one field?
       ↓
@field_validator

Rule involving multiple fields?
       ↓
@model_validator
```

This is one of the most important Day 5 concepts.

---

# 14. `model_dump()`

## What is it?

`model_dump()` converts a Pydantic model into a Python dictionary.

```python
order.model_dump()
```

Result:

```python
{
    "item": "Laptop",
    "quantity": 2
}
```

## Why?

FastAPI gives your service a Pydantic model:

```python
async def create_order_service(order):
```

Sometimes the service needs ordinary Python data.

Therefore:

```python
order.model_dump()
```

converts:

```text
Pydantic Model
      ↓
Python dict
```

---

# 15. Our Project Usage of `model_dump()`

In the product service:

```python
async def add_product_service(product):
    new_id = max(item["id"] for item in products) + 1

    product_data = product.model_dump()

    new_product = {
        "id": new_id,
        **product_data
    }

    products.append(new_product)

    return new_product
```

If the Pydantic model contains:

```python
supplier=suppelier(
    name="ABC",
    place="Hyderabad"
)
```

`model_dump()` also converts the nested Pydantic model into dictionary data:

```python
{
    "item": "Laptop",
    "category": "Electronics",
    "price": 50000,
    "stock": 10,
    "Discount_price": 45000,
    "supplier": {
        "name": "ABC",
        "place": "Hyderabad"
    }
}
```

---

# 16. Dictionary Unpacking with `**`

We used:

```python
new_product = {
    "id": new_id,
    **product_data
}
```

If:

```python
product_data = {
    "item": "Laptop",
    "price": 50000
}
```

then:

```python
{
    "id": 1,
    **product_data
}
```

becomes:

```python
{
    "id": 1,
    "item": "Laptop",
    "price": 50000
}
```

So:

```text
model_dump()
      ↓
dict
      ↓
**dict
      ↓
merge into another dict
```

---

# 17. `model_dump_json()`

The correct Pydantic v2 method is:

```python
model_dump_json()
```

Not:

```python
model_json_dump()
```

It converts a Pydantic model into a JSON string.

Example:

```python
order_json = order.model_dump_json()
```

Result:

```text
{"item":"Laptop","quantity":2}
```

### Difference

```text
model_dump()
      ↓
Python dictionary

model_dump_json()
      ↓
JSON string
```

---

# 18. Real-World Use of `model_dump_json()`

Suppose an external system expects a JSON string:

```python
async def send_order(order):
    order_json = order.model_dump_json()

    # Send order_json to an external system
```

It can also be useful for specific serialization or logging requirements.

For normal FastAPI responses, manually calling `model_dump_json()` is usually unnecessary because FastAPI already handles JSON serialization.

---

# 19. `include`

`include` means:

> Keep only these fields.

Example:

```python
product.model_dump(
    include={"item", "price", "stock"}
)
```

Result:

```python
{
    "item": "Laptop",
    "price": 50000,
    "stock": 10
}
```

Mental model:

```text
include
   ↓
KEEP selected fields
```

---

# 20. `exclude`

`exclude` means:

> Remove these fields.

Example:

```python
product.model_dump(
    exclude={"supplier"}
)
```

Mental model:

```text
exclude
   ↓
REMOVE selected fields
```

---

# 21. `exclude_none`

This removes fields whose value is `None`.

Example:

```python
model.model_dump(exclude_none=True)
```

If the model contains:

```python
{
    "name": "Uma",
    "email": None,
    "phone": "9876543210"
}
```

the result can be:

```python
{
    "name": "Uma",
    "phone": "9876543210"
}
```

### Real-world use

Useful when APIs should omit optional fields that are not available instead of returning unnecessary `null` values.

---

# 22. `exclude_unset`

This removes fields that were not explicitly supplied when the Pydantic model was created.

This is especially useful for partial updates.

Example model:

```python
class ProductUpdate(BaseModel):
    item: str | None = None
    price: int | None = None
    stock: int | None = None
```

Client sends:

```json
{
    "price": 45000
}
```

Then:

```python
product.model_dump(exclude_unset=True)
```

can produce:

```python
{
    "price": 45000
}
```

This allows an update service to change only the fields the client actually sent.

---

# 23. Why We Are Not Forcing These Options Into Our Current Project

Our current project is:

```text
FastAPI
   ↓
Pydantic
   ↓
Service
   ↓
Python list
```

There is currently no strong requirement for:

```python
include
exclude
exclude_none
exclude_unset
```

So we understand and document them without artificially adding them.

This is a professional engineering principle:

> Do not add a feature just because you learned it. Use it when the application actually needs it.

---

# 24. Industry Usage

## `@field_validator`

Used for:

- username normalization
- phone validation
- custom password rules
- product codes
- trimming strings
- custom field constraints

## `@model_validator`

Used for:

- password confirmation
- start date < end date
- discount <= price
- minimum <= maximum
- conditional fields
- dependent fields

## Regex

Used for:

- usernames
- employee IDs
- product codes
- policy numbers
- phone numbers
- PIN/postal codes
- API versions
- structured identifiers

## `model_dump()`

Used for:

- converting Pydantic models to Python dictionaries
- preparing service-layer data
- database operations
- data transformations
- passing structured data between application layers

## `model_dump_json()`

Used for:

- external API integrations
- JSON-string based systems
- message/event serialization
- specific logging/serialization requirements

## `include` / `exclude`

Used for:

- response shaping
- hiding fields
- selecting fields for different consumers
- controlling serialized data

Example:

```python
user.model_dump(exclude={"password"})
```

## `exclude_none`

Used for:

- clean API responses
- optional fields
- avoiding unnecessary `null` values

## `exclude_unset`

Used for:

- PATCH APIs
- partial updates
- identifying fields supplied by the client
- update services

---

# 25. Security Example

Suppose a user model contains:

```python
{
    "id": 10,
    "username": "uma",
    "password": "secret123"
}
```

A response should not expose the password.

One possible serialization approach:

```python
user.model_dump(
    exclude={"password"}
)
```

Result:

```python
{
    "id": 10,
    "username": "uma"
}
```

Important: password security requires more than serialization. Real applications should securely hash passwords and should never return password values to clients.

---

# 26. Day 5 Architecture in Our Project

Current structure:

```text
day_5/
│
├── main.py
│
├── routers/
│   ├── products.py
│   └── orders.py
│
├── services/
│   ├── products.py
│   └── orders.py
│
└── schemas/
    └── schema.py
```

Request flow:

```text
Client
  ↓
Router
  ↓
Pydantic Schema
  ↓
Validation
  ├── Field
  ├── Regex
  ├── field_validator
  └── model_validator
  ↓
Service
  ↓
model_dump()
  ↓
Python data
  ↓
Business operation
```

---

# 27. Complete Mental Model

```text
                 Pydantic Model
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Field()         Regex       Validators
        │              │          /               ↓              ↓         ↓         ↓
Basic constraints  Text format  Field     Model
                               validator validator
                                  │         │
                                  ↓         ↓
                             One field   Multiple fields
        │
        └──────────────────────┐
                               ↓
                         Serialization
                         /                                    ↓              ↓
                model_dump()   model_dump_json()
                        ↓              ↓
                    Python dict     JSON string
```

---

# 28. Day 5 Interview Questions

### What is `@field_validator`?

A Pydantic decorator for custom validation of one or more individual fields.

### What is `@model_validator`?

A Pydantic decorator for validation involving the model as a whole, especially relationships between fields.

### When should Regex be used?

When a string needs to follow a defined structural format.

### What does `model_dump()` return?

A Python dictionary.

### What does `model_dump_json()` return?

A JSON string.

### Difference between `include` and `exclude`?

```text
include → keep selected fields
exclude → remove selected fields
```

### What does `exclude_none=True` do?

Removes fields whose value is `None`.

### What does `exclude_unset=True` do?

Excludes fields that were not explicitly provided when the model was created. This is particularly useful for partial updates.

### Why not put `HTTPException` in the service?

HTTP-specific behavior belongs to the router/API layer. The service should focus on business logic.

---

# 29. Day 5 Completion Checklist

- [x] `@field_validator`
- [x] Multiple-field validation
- [x] `@model_validator`
- [x] Cross-field validation
- [x] Regex fundamentals
- [x] Username Regex
- [x] Password Regex
- [x] Lookahead Regex concept
- [x] Pydantic v2 Regex limitation
- [x] `model_dump()`
- [x] Practical `model_dump()` usage
- [x] Dictionary unpacking with `**`
- [x] `model_dump_json()`
- [x] `include`
- [x] `exclude`
- [x] `exclude_none`
- [x] `exclude_unset`
- [x] Industry use cases
- [x] Project architecture
- [x] Validation decision-making

---

# 30. Final Day 5 Principle

Do not memorize Pydantic features as isolated functions.

Choose the feature based on the problem:

```text
Need basic constraints?
→ Field()

Need string format validation?
→ Regex

Need custom validation for a field?
→ @field_validator

Need validation involving multiple fields?
→ @model_validator

Need Python dictionary?
→ model_dump()

Need JSON string?
→ model_dump_json()

Need selected fields?
→ include / exclude

Need to remove None values?
→ exclude_none

Need only client-provided fields?
→ exclude_unset
```

The goal of Day 5 is not simply to know Pydantic syntax.

The goal is to understand **which tool solves which backend problem and where that tool belongs in a real FastAPI application.**
