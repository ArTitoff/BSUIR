from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from routes import game, customers, timer, menu, employee, orders, hall
import models

app = FastAPI()

# Подключение маршрутов
app.include_router(game.router)
app.include_router(customers.router)
app.include_router(menu.router)
app.include_router(employee.router)
app.include_router(orders.router)
app.include_router(hall.router)

# Подключаем статические файлы и шаблоны с правильными путями
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "game_active": models.game_active}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)