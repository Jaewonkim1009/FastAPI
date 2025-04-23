from typing import Union
from fastapi import APIRouter

router = APIRouter(
    prefix="/sales",
    tags=["sales"],
    responses={404: {"에러발생" : "404 Not found"}}
)

@router.get("/{sales_id}")
def sales_user(sales_id : str):
    return {"sales_id" : sales_id}