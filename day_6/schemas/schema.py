from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
import re

class suppelier(BaseModel):
    name:str = Field(description="The name of the supplier")
    place:str = Field(description="The location of the supplier")

    @field_validator("name","place")
    @classmethod
    def name_validator(cls,value):
        value = value.strip()
        if not value:
            raise ValueError("Please enter a valid name or place.")
        return value

class createproduct(BaseModel):
    model_config = ConfigDict(strict=True)
    item:str = Field(description="The name of the product")
    category:str = Field(description="The category of the product")
    price:int = Field(description="The price of the product")
    stock:int = Field(default=0, description="The stock quantity of the product")
    Discount_price:int = Field(default=0, description="The discount price of the product")
    supplier:suppelier = Field(description="The supplier information for the product")

    @field_validator("item")
    @classmethod
    def vaidate_item(cls,value):
        value=value.strip()
        if not value:
            raise ValueError("Please enter a valid item name.")
        if len(value)<3:
            raise ValueError("Item name must be at least 3 characters long.")
        return value

    @field_validator("category")
    @classmethod
    def validate_category(cls,value):
        value=value.strip()
        if not value:
            raise ValueError("Please enter a valid category.")
        
        if len(value)<3:
            raise ValueError("Category name must be at least 3 characters long.")
        return value
    
    @field_validator("price","stock",)
    @classmethod
    def validate_price_and_stock(cls,value):
        if value < 0:
            raise ValueError("Price and stock must be positive integers.")
        return value

    @field_validator("Discount_price")
    @classmethod
    def validate_discount_price(cls,value):
        if value < 0:
            raise ValueError("Discount price must be a positive integer.")
        return value

    @model_validator(mode="after")
    def validate_discount_against_price(self):
        if self.Discount_price > self.price:
            raise ValueError("Discount price cannot be greater than the original price.")  
        return self
    
class updateproduct(BaseModel):
    id:int = Field(description="The ID of the product to update")
    item:str = Field(description="The name of the product")
    category:str = Field(description="The category of the product")
    price:int = Field(description="The price of the product")
    stock:int = Field(description="The stock quantity of the product", default=0)
    Discount_price:int = Field(default=0, description="The discount price of the product")
    supplier:suppelier = Field(description="The supplier information for the product")

    @field_validator("item")
    @classmethod
    def vaidate_item(cls,value):
        value=value.strip()
        if not value:
            raise ValueError("Please enter a valid item name.")
        if len(value)<3:
            raise ValueError("Item name must be at least 3 characters long.")
        return value

    @field_validator("category")
    @classmethod
    def validate_category(cls,value):
        value=value.strip()
        if not value:
            raise ValueError("Please enter a valid category.")
        
        if len(value)<3:
            raise ValueError("Category name must be at least 3 characters long.")
        return value
    @field_validator("id","price","stock","Discount_price")
    @classmethod
    def validate_id_price_and_stock(cls,value):
        if value <= 0:
            raise ValueError("ID, price, stock and Discount price must be positive integers.")
        return value
    
    @model_validator(mode="after")
    def validate_discount_against_price(self):
        if self.Discount_price > self.price:
            raise ValueError("Discount price cannot be greater than the original price.")  
        return self

class createorder(BaseModel):
    item:str = Field(description="The name of the order")
    quantity:int = Field(description="The quantity of the order", default=0)

    @field_validator("item")
    @classmethod
    def validate_item(cls,value):
        value=value.strip()
        if not value:
            raise ValueError("Please enter a valid item name.")
        if len(value)<3:
            raise ValueError("Item name must be at least 3 characters long.")
        return value
    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls,value):
        if value <= 0:
            raise ValueError("Quantity must be a positive integer.")
        return value

class updateorder(BaseModel):
    id:int = Field(description="The ID of the order to update")
    item:str = Field(description="The name of the order")
    quantity:int = Field(description="The quantity of the order", default=0)

    @field_validator("item")
    @classmethod
    def validate_item(cls,value):
        value=value.strip()
        if not value:
            raise ValueError("Please enter a valid item name.")
        if len(value)<3:
            raise ValueError("Item name must be at least 3 characters long.")
        return value
    @field_validator("id","quantity")
    @classmethod
    def validate_id_and_quantity(cls,value):
        if value < 0:
            raise ValueError("ID and quantity must be positive integers.")
        return value

class createuser(BaseModel):
    username:str = Field(description="The username of the user",min_length=3,max_length=20,pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    password:str = Field(description="The password of the user",min_length=6,max_length=20,)

    @field_validator("username")
    @classmethod
    def validate_username(cls,value):
        value=value.strip()

        if not value:
            raise ValueError("Please enter a valid username.")
        if len(value)<3:
            raise ValueError("Username must be at least 3 characters long.")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls,value):
        value=value.strip()
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(pattern, value):
            raise ValueError("Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
        if not value:
            raise ValueError("Please enter a valid password.")
        if len(value)<6:
            raise ValueError("Password must be at least 6 characters long.")
        return value

    