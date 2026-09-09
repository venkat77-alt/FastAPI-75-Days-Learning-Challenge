from fastapi import APIRouter
from schemas.schema import createuser

users=[
    {
        "username": "venkat",
        "password":"Venkat@123"
    }
]

router = APIRouter()

@router.post("/")
async def login(credentials:createuser):
    for user in users:
        if user["username"] == credentials.username and user["password"] == credentials.password:
            return {"message": "Login successful"}
    return {"message": "Invalid username or password"}