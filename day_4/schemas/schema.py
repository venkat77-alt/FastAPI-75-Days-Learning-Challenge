from pydantic import BaseModel, Field, ConfigDict

class suppelier(BaseModel):
    name:str = Field(description="The name of the supplier")
    place:str = Field(description="The location of the supplier")

class createproduct(BaseModel):
    model_config = ConfigDict(strict=True)
    item:str = Field(description="The name of the product")
    category:str = Field(description="The category of the product")
    price:int = Field(description="The price of the product")
    stock:int = Field(default=0, description="The stock quantity of the product")
    supplier:suppelier = Field(description="The supplier information for the product")



class updateproduct(BaseModel):
    id:int = Field(description="The ID of the product to update")
    item:str = Field(description="The name of the product")
    category:str = Field(description="The category of the product")
    price:int = Field(description="The price of the product")
    stock:int = Field(description="The stock quantity of the product", default=0)
    supplier:suppelier = Field(description="The supplier information for the product")

class createorder(BaseModel):
    item:str = Field(description="The name of the order")
    quantity:int = Field(description="The quantity of the order", default=0)

class updateorder(BaseModel):
    id:int = Field(description="The ID of the order to update")
    item:str = Field(description="The name of the order")
    quantity:int = Field(description="The quantity of the order", default=0)