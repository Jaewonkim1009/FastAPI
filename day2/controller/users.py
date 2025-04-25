from typing import Union
from fastapi import APIRouter

router = APIRouter(
    prefix = "/users",
    tags = ["users"],
    responses = {404 : {"에러 발생" : "404 Not Found"}}
)

@router.get("/{users_id}")
def read_users(user_id: int):
    return {"user_id" : user_id}