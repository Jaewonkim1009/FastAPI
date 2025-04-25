from typing import Union
from fastapi import APIRouter

router = APIRouter(
    prefix="/marketing",
    tags=["marketing"],
    responses={404: {"에러발생" : "404 Not found"}}
)

@router.get("/{marketing}")
def marketing_list(marketing : int):
    return {marketing : marketing}