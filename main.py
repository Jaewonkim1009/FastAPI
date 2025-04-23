from typing import Union
from fastapi import FastAPI
# 컨트롤러와 연결
from controller import items, users, sales, admins


app = FastAPI()

# 컨트롤러에서 작성한 컨트롤러.py의 router 불러오기
app.include_router(items.router)
app.include_router(users.router)
app.include_router(sales.router)
app.include_router(admins.router)

@app.get("/")
def read_root():
    return {"Hello" : "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None): # Union : 타입을 확인
#     return {"item_id" : item_id, "q" : q}