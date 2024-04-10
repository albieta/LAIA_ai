from fastapi import APIRouter
from typing import List

general_routes_router = APIRouter()

@general_routes_router.get('/somthing/')
async def get_something():

    return {"message": "Action created successfully"}