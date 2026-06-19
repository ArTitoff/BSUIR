import asyncio
from fastapi import APIRouter
import models

router = APIRouter()

async def run_timer():
    print("Таймер запущен")
    while models.game_state["time_left"] > 0 and models.game_state:
        await asyncio.sleep(1)
        models.game_state["time_left"] -= 1
        print(f"Таймер: {models.game_state['time_left']} секунд осталось")
    models.game_active = False
    print("Таймер остановлен")
