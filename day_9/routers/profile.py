from dependencies.current_user import get_current_user
from dependencies.admin import is_admin
from fastapi import Depends,APIRouter
from services.profile import get_user_profile,account_active_status 


router=APIRouter()

@router.get("/current_user")
async def profile(current_user=Depends(get_current_user)):
    profile=await get_user_profile(current_user)
    return profile

@router.get("/status")
async def account_status(current_user=Depends(get_current_user)):
    status=await account_active_status(current_user)
    return status

@router.get("/is_admin")
async def is_user_admin(is_admin=Depends(is_admin)):
    return is_admin
