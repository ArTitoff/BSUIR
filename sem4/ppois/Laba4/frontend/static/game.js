// Выключение кнопок после завершения игры
function disableButtons() {
    document.getElementById("hall").disabled = true;
    document.getElementById("orders").disabled = true;
}

// Считывание текущего состояния
function startPolling() {
    setInterval(() => {
        if (gameActive) {
            fetchGameState();
            fetchOrders();
            fetchTables();
        }

    }, 500);
}

// Старт игры
async function startGame() {
    try {
        // Запрос списка блюд
        const dishesResponse = await fetch('/api/dishes', { method: 'GET' });
        const dishesData = await dishesResponse.json();

        // Проверка, есть ли блюда (предполагаем, что это массив)
        if (dishesData.length === 0) {
            alert("Нет блюд в меню");
            return; // Прерываем выполнение, если блюд нет
        }

        // Запуск игры
        startPanel.classList.add("hidden");
        const gameResponse = await fetch('/api/start_game', { method: 'POST' });
        const gameData = await gameResponse.json();

        if (gameData.success) {
            gameActive = true;
            document.getElementById("orders").disabled = false;
            document.getElementById("hall").disabled = false;
            document.getElementById("employee").disabled = true;
            document.getElementById("menu").disabled = true;
            startGameBtn.disabled = true;
            startPolling();
        } else {
            console.error("Ошибка при запуске игры:", gameData);
        }
    } catch (error) {
        console.error("Ошибка при запуске игры:", error);
        alert("Произошла ошибка. Проверьте консоль для деталей.");
    }
}