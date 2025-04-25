from typing import Union
from fastapi import FastAPI
from controller import marketing, products, sales, users
from pydantic import BaseModel
from calculator import calculate_sale
app = FastAPI()

@app.get("/")
def read_root():
    return {"판매 시스템"}

app.include_router(marketing.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(users.router)

class Product(BaseModel):
    items: str
    x: float
    y: float

@app.post("/calculate_sale")
def calculate(product: Product):
    result = calculate_sale(product.items, product.x * 1000, product.y)
    return {"result": result}
