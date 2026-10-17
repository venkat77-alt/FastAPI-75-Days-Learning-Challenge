
async def get_current_user():
    try:
        yield {
            "id":101,
            "user_name":"venkat",
            "role":"Admin",
            "status":"Active"
        }
    finally:
        print("Current user check completed")