from typing import Union
from fastapi import APIRouter

router = APIRouter(
    prefix = "/products",
    tags=["products"],
    responses = {404 : {"에러 발생" : "404 Not Found"}}
)

@router.get("/{products}")
def read_products(products: int):
    return {"products" : products}