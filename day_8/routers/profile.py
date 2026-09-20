from dependencies.current_user import get_current_user
from fastapi import Depends,APIRouter
from services.profile import get_user_profile

router=APIRouter()

@router.get("/")
async def profile(current_user=Depends(get_current_user)):
    profile=await get_user_profile(current_user)
    return profile