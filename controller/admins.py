from fastapi import APIRouter
from model import pgsql_test

router = APIRouter (
    prefix="/admins",
    tags=["admins"],
    responses={404: {"descrition": "Not found"}}
)

@router.get("/list")
def list_admin():
    results = pgsql_test.list_admin()
    return results