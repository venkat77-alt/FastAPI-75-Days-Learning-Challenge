from dependencies.current_user import get_current_user
from fastapi import Depends,HTTPException
async def is_admin(admin=Depends(get_current_user)):
    try:
        if admin["role"] !="Admin":
            raise HTTPException(
                status_code=403,
                detail={
                    "message":"Admin required"
                }
            )
        yield admin
    finally:
        print("Admin check completed")