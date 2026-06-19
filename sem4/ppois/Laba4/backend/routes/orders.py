import asyncio
import random
from fastapi import APIRouter
import models

router = APIRouter()

# Список заказов в памяти (можно заменить на базу данных)
orders = [
    # Пример структуры: { "table": номер_столика, "dish": название_блюда, "completed": состояние }
    # {"table": 1, "dish": "Борщ", "completed": False},
    # {"table": 2, "dish": "Пельмени", "completed": True}
]

@router.get("/api/orders")
async def get_orders():
    return orders

# Приготовление заказа
@router.post("/api/cook_order")
async def cook_order(order: dict):
    table = order.get("table")
    dish = order.get("dish")
    for o in orders:
        if o["table"] == table and o["dish"] == dish and not o["completed"]:
            o["completed"] = True
            return {"success": True, "message": f"Заказ '{dish}' для столика {table} приготовлен"}
    return {"success": False, "message": "Заказ не найден или уже приготовлен"}

def add_order(table: int, dish: str):
    orders.append({"table": table+1, "dish": dish, "completed": False})