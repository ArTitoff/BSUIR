import asyncio
import random
from fastapi import APIRouter
import models

router = APIRouter()

employees = []  # Список нанятых сотрудников

@router.post("/api/hire_employee")
async def hire_employee(employee: dict):
    name = employee.get("name")
    cost = employee.get("cost")
    if name not in employees and models.game_state["money"] >= cost:
        employees.append(name)
        models.game_state["money"] -= cost  # Вычитаем стоимость найма
        return {"success": True}
    elif name in employees:
        return {"success": False, "message": "Сотрудник уже нанят"}
    else:
        return {"success": False, "message": "Недостаточно денег"}

@router.get("/api/employees")
async def get_employees():
    return employees