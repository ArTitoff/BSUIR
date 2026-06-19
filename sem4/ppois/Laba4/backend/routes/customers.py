import asyncio
import random
from fastapi import APIRouter
import models
import routes.hall
import routes.orders
import routes.menu

router = APIRouter()

max_customers = 5
customers_range = 0.1

async def spawn_customers():
    while models.game_state["time_left"] > 0 and models.game_active and len(routes.menu.dishes) > 0:
        if random.random() > customers_range and models.game_state["customers"] < max_customers:
            free_tables = [i for i, table in enumerate(routes.hall.tables) if not table["occupied"]]
            if free_tables:
                table_index = random.choice(free_tables)
                routes.hall.tables[table_index]["occupied"] = True
                models.game_state["customers"] += 1
                models.game_state["orders"] += 1
                routes.orders.add_order(table_index, routes.menu.dishes[random.randint(0, len(routes.menu.dishes) - 1)])
        await asyncio.sleep(3)