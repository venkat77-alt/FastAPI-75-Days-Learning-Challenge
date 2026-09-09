from fastapi import APIRouter, Query,Path
from services.products import get_products_service,get_product_service,add_product_service,update_product_service,delete_product_service
from fastapi import HTTPException
from schemas.schema import createproduct,updateproduct

router=APIRouter()

@router.get("/")
async def get_products(
        search,
        category,
        min_price,
        max_price
):

    product=await get_products_service(search,category,min_price,max_price)

    return product


@router.get("/{id}")
async def get_product(id:int=Path(..., description="The ID of the product to retrieve",ge=1, le=9999)):
    product=await get_product_service(id)
    if product:
        return product
    else:
        raise HTTPException(
            status_code=404,
            detail="product not found"
        )

@router.post("/")
async def post_product(product:createproduct):
    new_product=await add_product_service(product)
    return {
        "message": "The product created successfully",
        "product": new_product
    }

@router.put("/{id}")
async def update_product(updateproduct:updateproduct):
    updated_product=await update_product_service(updateproduct)
    if updated_product:
        return {
            "message": "The product updated successfully",
            "product": updated_product
        }
    else:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

@router.delete("/{id}")
async def delete_product(id:int=Path(..., description="The ID of the product to delete",ge=1, le=9999)):
    
    result=await delete_product_service(id)
    if result:
        return {
            "message": "The product deleted successfully",
            "product": result
        }
    else:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

@router.get("/test-error/{num}")
async def test_error(num:int):

    result = num / 0

    return result