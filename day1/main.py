from typing import Union
from fastapi import FastAPI
# 컨트롤러와 연결
from controller import items, users, sales, admins
from day1.calculator import calculate
# 데이터 검증과 직렬화를 위함
from pydantic import BaseModel


app = FastAPI()

# 컨트롤러에서 작성한 컨트롤러.py의 router 불러오기
# main과 controller 연결
app.include_router(items.router)
app.include_router(users.router)
app.include_router(sales.router)
app.include_router(admins.router)

@app.get("/")
def read_root():
    return {"Hello" : "World"}

# JSON 데이터를 직렬화
class User_input(BaseModel):
    operation : str
    x : float
    y : float

@app.post("/calculate")
def operate(input: User_input):
    result = calculate(input.operation, input.x, input.y)
    return result

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None): # Union : 타입을 확인
#     return {"item_id" : item_id, "q" : q}