from pydantic import BaseModel
from schemas.request_schema import suppelier



class productsResponse(BaseModel):
    id:int
    item:str
    category:str
    price:int
    stock:int
    Discount_price:int

class productcreateobject(BaseModel):
    id: int
    item: str
    category: str
    price: int
    stock: int
    Discount_price: int
    supplier: suppelier

class productcreateresponse(BaseModel):
    message:str
    product:productcreateobject

class orderResponse(BaseModel):
    id:int
    item:str
    quantity:int

class ordercreateresponse(BaseModel):
    message:str
    order:orderResponse

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