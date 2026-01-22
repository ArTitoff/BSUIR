// Обновление статусов
function updateUI(data) {
    cashElement.textContent = data.money;
    timeElement.textContent = data.time_left;
    customersElement.textContent = data.customers > 0
        ? `Клиентов: ${data.customers}, заказов: ${data.orders}`
        : "Клиентов нет";
}

// Получение информации об игре
async function fetchGameState() {
    try {
        const response = await fetch('/api/game_state');
        const data = await response.json();
        updateUI(data);

        if (data.time_left <= 0 && gameActive) {
            gameActive = false;
            alert(`Игра окончена! Заработано: ${data.money} рублей`);
            disableButtons();
            document.getElementById("employee").disabled = false;
            document.getElementById("menu").disabled = false;
            startGameBtn.disabled = false;
        }
    } catch (error) {
        console.error("Ошибка при получении состояния игры:", error);
    }
}

async function checkGameStateOnLoad() {
    try {
        const response = await fetch('/api/game_state');
        const data = await response.json();
        if (data.time_left > 0) { // Если время ещё осталось, игра активна
            gameActive = true;
            startPolling(); // Запускаем polling
        }
    } catch (error) {
        console.error("Ошибка при проверке состояния игры:", error);
    }
}

// Вызов при загрузке страницы
window.onload = checkGameStateOnLoad;