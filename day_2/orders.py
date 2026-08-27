from fastapi import APIRouter
from fastapi import Query as query
from fastapi import Path as path



router = APIRouter()


orders = [
    {
        "id": 1,
        "item": "mobile",
        "quantity": 1
    },
    {
        "id": 2,
        "item": "mobile",
        "quantity": 2
    },
    {
        "id": 3,
        "item": "mobile",
        "quantity": 5
    },
    {
        "id": 4,
        "item": "laptop",
        "quantity": 1
    },
    {
        "id": 5,
        "item": "laptop",
        "quantity": 2
    },
    {
        "id": 6,
        "item": "laptop",
        "quantity": 3
    },
    {
        "id": 7,
        "item": "tablet",
        "quantity": 1
    },
    {
        "id": 8,
        "item": "tablet",
        "quantity": 2
    },
    {
        "id": 9,
        "item": "tablet",
        "quantity": 4
    },
    {
        "id": 10,
        "item": "headphones",
        "quantity": 1
    },
    {
        "id": 11,
        "item": "headphones",
        "quantity": 2
    },
    {
        "id": 12,
        "item": "headphones",
        "quantity": 5
    },
    {
        "id": 13,
        "item": "keyboard",
        "quantity": 1
    },
    {
        "id": 14,
        "item": "keyboard",
        "quantity": 3
    },
    {
        "id": 15,
        "item": "mouse",
        "quantity": 2
    },
    {
        "id": 16,
        "item": "mouse",
        "quantity": 5
    },
    {
        "id": 17,
        "item": "monitor",
        "quantity": 1
    },
    {
        "id": 18,
        "item": "monitor",
        "quantity": 2
    },
    {
        "id": 19,
        "item": "smartwatch",
        "quantity": 1
    },
    {
        "id": 20,
        "item": "smartwatch",
        "quantity": 3
    }
]
@router.get("/")
async def get_orders(
    search:str | None= query(None, min_length=3, max_length=50, description="Search for orders by item name"),
    

):
    filtered_product=[]

    for order in orders:
        if search is not None:
            if search.lower() not in order["item"].lower():
                continue


        filtered_product.append(order)

    return filtered_product


@router.get("/{order_id}")
async def get_order(order_id: int|None = path(..., description="The ID of the order to retrieve",ge=1, le=9999)):
    for order in orders:
        if order["id"] == order_id:
            return order
    return {
        "message": "Order not found"
            }