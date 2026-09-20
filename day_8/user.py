from fastapi import APIRouter
from schemas.request_schema import validate_user,create_user
from schemas.response_schema import UserCreateResponse,LoginResponse
users=[
    {
        "id":1,
        "username": "venkat",
        "password":"Venkat@123",
        "role":"admin"

    }
]

router = APIRouter()

@router.post("/create/user",response_model=UserCreateResponse,response_model_exclude_unset=True)
async def create_user(credentials: create_user):

    user_id = max(user["id"] for user in users) + 1

    new_user = {
        "id": user_id,
        **credentials.model_dump()
    }

    for user in users:
        if user["username"] == credentials.username:
            return {"message": "User already exists"}

    users.append(new_user)

    return {
        "message": "User created successfully",
        "user": new_user
    }

@router.post("/login",response_model=LoginResponse)
async def login(credentials:validate_user):
    for user in users:
        if user["username"] == credentials.username and user["password"] == credentials.password:
            return {"message":"Login successful"}
                   
    return {"message": "Invalid username or password"}