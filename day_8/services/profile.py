
async def get_user_profile(current_user):
    return {
        "id":current_user["id"],
        "user_name":current_user["user_name"],
        "role":current_user["role"],
        "profile":{
            "name":"venkat",
            "email":"venkat@gmail.com",
            "Mobile number":9887654321
        }
    }