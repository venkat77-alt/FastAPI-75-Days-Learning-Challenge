from fastapi import Query as query
from fastapi import Path as path
from schemas.schema import createproduct,updateproduct


products = [
    {
        "id": 1,
        "item": "mobile",
        "category": "electronics",
        "price": 10000,
        "stock": 20,
        "Discount_price": 2000,
        "supplier": {
            "name": "ABC Electronics",
            "place": "New York",

        }
    },
    {
        "id": 2,
        "item": "mobile",
        "category": "electronics",
        "price": 12000,
        "stock": 15,
        "Discount_price": 2400,
        "supplier": {
            "name": "XYZ Tech",
            "place": "Los Angeles"
        }
    },
    {
        "id": 3,
        "item": "mobile",
        "category": "electronics",
        "price": 15000,
        "stock": 8,
        "Discount_price": 3000,
        "supplier": {
            "name": "DEF Innovations",
            "place": "Chicago"
        }
    },
    {
        "id": 4,
        "item": "laptop",
        "category": "electronics",
        "price": 50000,
        "stock": 10,
        "Discount_price": 10000,
        "supplier": {
            "name": "GHI Solutions",
            "place": "Miami"
        }
    },
    {
        "id": 5,
        "item": "laptop",
        "category": "electronics",
        "price": 55000,
        "stock": 7,
        "Discount_price": 11000,
        "supplier": {
            "name": "JKL Enterprises",
            "place": "Seattle"
        }
    },
    {
        "id": 6,
        "item": "laptop",
        "category": "electronics",
        "price": 65000,
        "stock": 5,
        "Discount_price": 13000,
        "supplier": {
            "name": "MNO Technologies",
            "place": "Denver"
        }
    },
    {
        "id": 7,
        "item": "tablet",
        "category": "electronics",
        "price": 20000,
        "Discount_price": 4000,
        "stock": 15,
        "supplier": {
            "name": "PQR Devices",
            "place": "Austin"
        }
    },
    {
        "id": 8,
        "item": "tablet",
        "category": "electronics",
        "price": 25000,
        "stock": 10,
        "Discount_price": 5000,
        "supplier": {
            "name": "STU Gadgets",
            "place": "Boston"
        }
    },
    {
        "id": 9,
        "item": "tablet",
        "category": "electronics",
        "price": 30000,
        "Discount_price": 6000,
        "stock": 6,
        "supplier": {
            "name": "VWX Accessories",
            "place": "San Francisco"
        }
    },
    {
        "id": 10,
        "item": "headphones",
        "category": "audio",
        "price": 3000,
        "stock": 30,
        "Discount_price": 600,
        "supplier": {
            "name": "YZA Audio",
            "place": "Seattle"
        }
    },
    {
        "id": 11,
        "item": "headphones",
        "category": "audio",
        "price": 5000,
        "stock": 20,
        "Discount_price": 1000,
        "supplier": {
            "name": "YZA Audio",
            "place": "Seattle"
        }
    },
    {
        "id": 12,
        "item": "headphones",
        "category": "audio",
        "price": 8000,
        "stock": 12,
        "Discount_price": 1600,
        "supplier": {
            "name": "YZA Audio",
            "place": "Seattle"
        }
    },
    {
        "id": 13,
        "item": "keyboard",
        "category": "computer_accessories",
        "price": 2500,
        "stock": 25,
        "Discount_price": 500,
        "supplier": {
            "name": "ABC Electronics",
            "place": "New York"
        }
    },
    {
        "id": 14,
        "item": "keyboard",
        "category": "computer_accessories",
        "price": 3500,
        "stock": 18,
        "Discount_price": 700,
        "supplier": {
            "name": "ABC Electronics",
            "place": "New York"
        }
    },
    {
        "id": 15,
        "item": "mouse",
        "category": "computer_accessories",
        "price": 1500,
        "stock": 40,
        "Discount_price": 300,
        "supplier": {
            "name": "DEF Innovations",
            "place": "Chicago"
        }
    },
    {
        "id": 16,
        "item": "mouse",
        "category": "computer_accessories",
        "price": 2500,
        "stock": 25,
        "Discount_price": 500,
        "supplier": {
            "name": "DEF Innovations",
            "place": "Chicago"
        }
    },
    {
        "id": 17,
        "item": "monitor",
        "category": "computer_accessories",
        "price": 15000,
        "stock": 12,
        "Discount_price": 1000,
        "supplier": {
            "name": "GHI Solutions",
            "place": "Miami"
        }
    },
    {
        "id": 18,
        "item": "monitor",
        "category": "computer_accessories",
        "price": 22000,
        "stock": 8,
        "Discount_price": 2000,
        "supplier": {
            "name": "GHI Solutions",
            "place": "Miami"
        }
    },
    {
        "id": 19,
        "item": "smartwatch",
        "category": "wearables",
        "price": 8000,
        "stock": 18,
        "Discount_price": 1000,
        "supplier": {
            "name": "JKL Enterprises",
            "place": "Seattle"
        }
    },
    {
        "id": 20,
        "item": "smartwatch",
        "category": "wearables",
        "price": 12000,
        "stock": 10,
        "Discount_price": 2000, 
        "supplier": {
            "name": "JKL Enterprises",
            "place": "Seattle"
        }
    }
]
    

async def get_products_service(
    search:str | None= query(None, min_length=3, max_length=50, description="Search for products by name"),
    category:str |None = query(None, min_length=3, max_length=50, description="Filter products by category"),
    min_price:int | None = query(None, ge=0, description="Filter products with a minimum price",le=9999999),
    max_price:int | None = query(None, ge=0, description="Filter products with a maximum price",le=9999999)
):
    filtered_product=[]

    for product in products:
        if search is not None:
            if search.lower() not in product["item"].lower():
                continue

        if category is not None:
            if product["category"] != category:
                continue

        if min_price is not None:
            if product["price"] < min_price:
                continue

        if max_price is not None:
            if product["price"] > max_price:
                continue

        filtered_product.append(product)
    return filtered_product


async def get_product_service(id : int|None = path(..., description="The ID of the product to retrieve",ge=1, le=9999)):
    for product in products:
        if product["id"]== id:
            return product
        return None

async def add_product_service(
    product:createproduct
):
    new_id=max(product["id"] for product in products)+1
    product_data=product.model_dump()
    new_product={
        "id":new_id,
        **product_data #this line is for unpacking the dictionary and adding its key-value pairs to the new_product dictionary by using model_dump() method of pydantic model to convert the model instance into a dictionary representation.
    }
    products.append(new_product)
    return new_product


async def update_product_service(
    updateproduct:updateproduct
):
    for product in products:
        if product["id"]==updateproduct.id:
            product["item"]=updateproduct.item
            product["category"]=updateproduct.category
            product["price"]=updateproduct.price
            product["stock"]=updateproduct.stock
            product["supplier"]=updateproduct.supplier
            return product
    return None

async def delete_product_service(id:int):
    for product in products:
        if product["id"]==id:

            products.remove(product)

            return product
        return None  