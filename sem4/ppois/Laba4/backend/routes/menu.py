import asyncio
import random
from fastapi import APIRouter
import models

router = APIRouter()

# Список блюд
dishes = []

@router.post("/api/add_dish")
async def add_dish(dish: dict):
    dish_name = dish.get("name")
    if dish_name and dish_name not in dishes:
        dishes.append(dish_name)
        return {"success": True}
    return {"success": False, "message": "Блюдо уже существует или название пустое"}

@router.get("/api/dishes")
async def get_dishes():
    return dishes

@router.post("/api/remove_dish")
async def remove_dish(dish: dict):
    dish_name = dish.get("name")
    if dish_name in dishes:
        dishes.remove(dish_name)
        return {"success": True}
    return {"success": False, "message": "Блюдо не найдено"}