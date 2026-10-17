from fastapi import HTTPException
async def get_user_profile(current_user):
    return {
        "id":current_user["id"],
        "user_name":current_user["user_name"],
        "role":current_user["role"],
        "status":current_user["status"],

        "profile":{
            "name":"venkat",
            "email":"venkat@gmail.com",
            "Mobile number":9887654321
        }
    }

async def account_active_status(current_user):
    if current_user["status"] != "Active":
        raise HTTPException(
            status_code=403,
            detail={
                "message":"Only active users can login"
            }
        )
    return current_user
    