from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    phone: str | None = None
    age: int | None = None

user = User(
    name="venkat reddy",
    email="venkat@example.com"
)

print(user.model_dump())
print(user.model_dump_json())

print(user.model_dump(include={"name", "email"}))
print(user.model_dump(exclude={"phone"}))

print(user.model_dump(exclude_none=True))