import asyncio
import random
from fastapi import APIRouter
import models
import routes.orders

router = APIRouter()

# Список столов с состоянием занятости
tables = [{"name": f"Стол {i}", "occupied": False} for i in range(1, 6)]

# Получение столов
@router.get("/api/tables")
async def get_tables():
    return tables

@router.post("/api/issue_order")
async def issue_order(order: dict):
    table_num = order.get("table") - 1  # Номер стола из запроса (уменьшаем на 1 для индекса)
    
    # Проверяем, есть ли активные заказы вообще и существует ли заказ для указанного стола
    if len(routes.orders.orders) > 0 and any(o.get("table") - 1 == table_num for o in routes.orders.orders):
        # Находим заказ для конкретного стола
        current_order = next((o for o in routes.orders.orders if o.get("table") - 1 == table_num), None)
        
        # Проверяем, что стол занят и заказ существует
        if current_order and tables[table_num]["occupied"]:
            # Проверяем, выполнен ли заказ (completed == True)
            if current_order.get("completed", False):
                models.game_state["orders"] -= 1
                models.game_state["customers"] -= 1
                models.game_state["money"] += 50
                tables[table_num]["occupied"] = False
                
                # Удаляем выполненный заказ из списка
                routes.orders.orders.remove(current_order)
                
                return {
                    "success": True,
                    "message": f"Стол {table_num + 1} обслужен, заработано 50 рублей"
                }
            else:
                return {
                    "success": False,
                    "message": f"Заказ для стола {table_num + 1} еще не выполнен"
                }
        return {
            "success": False,
            "message": "Стол не занят"
        }
    return {
        "success": False,
        "message": "Нет активных заказов или клиентов для стола"
    }