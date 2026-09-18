from fastapi import APIRouter, HTTPException
from fastapi import Query as query
from fastapi import Path as path

from schemas.schema import createorder, updateorder

from services.orders import (
    get_orders_service,
    get_order_service,
    create_order_service,
    update_order_service,
    delete_order_service
)


router = APIRouter()


@router.get("/")
async def get_orders(
    search: str | None = query(
        None,
        min_length=3,
        max_length=50,
        description="Search for orders by item name"
    )
):
    orders = await get_orders_service(search)

    return orders


@router.get("/{order_id}")
async def get_order(
    order_id: int = path(
        ...,
        description="The ID of the order to retrieve",
        ge=1,
        le=9999
    )
):
    order = await get_order_service(order_id)

    if order:
        return order

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )


@router.post("/")
async def create_order(order: createorder):

    new_order = await create_order_service(order)

    return {
        "message": "Order created successfully",
        "order": new_order
    }


@router.put("/{id}")
async def update_order(updateorders: updateorder):

    updated_order = await update_order_service(updateorders)

    if updated_order:
        return {
            "message": "Order updated successfully",
            "order": updated_order
        }

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )


@router.delete("/{id}")
async def delete_order(
    id: int = path(
        ...,
        description="The ID of the order to delete",
        ge=1,
        le=9999
    )
):

    deleted_order = await delete_order_service(id)

    if deleted_order:
        return {
            "message": "Order deleted successfully",
            "deleted_order": deleted_order
        }

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )