from fastapi import APIRouter,HTTPException
from fastapi import Query as query
from fastapi import Path as path


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

@router.get("/")
async def get_products(
    search:str | None= query(None, min_length=3, max_length=50, description="Search for products by name"),
    category:str |None =query(None, min_length=3, max_length=50, description="Filter products by category"),
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

@router.get("/{id}")
async def get_products(id : int|None = path(..., description="The ID of the product to retrieve",ge=1, le=9999)):
    for product in products:
        if product["id"]== id:
            return product
    raise HTTPException(
        status_code=404,
        detail="product not found"
    )

"=====posting a new product into exiting product list====="
@router.post("/")
async def add_product(
    item:str,
    category:str,
    price:int,
    stock:int
):
    new_id=max(product["id"] for product in products)+1

    new_product={
        "id":new_id,
        "item":item,
        "category":category,
        "price":price,
        "stock":stock
    }
    products.append(new_product)
    return {
        "message":"the product created successfully",
        "product":new_product
    }


"===updating a product==="
@router.put("/{id}")
async def update_product(
    id:int,
    item:str,
    category:str,
    price:int,
    stock:int
):
    for product in products:
        if product["id"]==id:
            product["item"]=item
            product["category"]=category
            product["price"]=price
            product["stock"]=stock
            return {
                "message":"product updated successfullly",
                "product":product
            }
    raise HTTPException(
        status_code=404,
        detail="product not found"
    )


"===deleting a product==="
@router.delete("/{id}")
async def delete_product(id:int):
    for product in products:
        if product["id"]==id:
            products.remove(product)

            return{
                "message":"product deleted successfully",
                "deleted_product":product
            }
    raise HTTPException(
        status_code=404,
        detail="product not found"
    )


"=====sample general exceptiion testing endpoint===="
@router.get("/test-error/{num}")
async def test_error(num:int):

    result = num / 0

    return result