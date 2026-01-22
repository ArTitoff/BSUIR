from fastapi import APIRouter
import asyncio
import models
from routes.customers import spawn_customers
from routes.timer import run_timer

router = APIRouter()

@router.get("/api/game_state")
async def get_game_state():
    return models.game_state

@router.post("/api/start_game")
async def start_game():
    models.game_state.update({"money": 0, "customers": 0, "orders": 0, "time_left": 60})
    models.game_active = True
    asyncio.create_task(spawn_customers())
    asyncio.create_task(run_timer())
    return {"success": True}

@router.post("/api/take_order")
async def take_order():
    if models.game_state["customers"] > 0 and models.game_state["orders"] > 0:
        models.game_state["orders"] -= 1
        return {"success": True, "message": "Заказ принят"}
    return {"success": False, "message": "Нет заказов для принятия"}

@router.post("/api/cook")
async def cook():
    return {"success": True, "message": "Еда готова"}

@router.post("/api/serve")
async def serve():
    if models.game_state["customers"] > 0:
        models.game_state["customers"] -= 1
        models.game_state["money"] += 50
        return {"success": True, "message": "Клиент обслужен"}
    return {"success": False, "message": "Нет клиентов для обслуживания"}
