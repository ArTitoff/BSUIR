// Обновление списка заказов
async function fetchOrders() {
    try {
        const orderListElement = document.getElementById("orderList"); // Явно определяем элемент
        const response = await fetch('/api/orders');
        const orders = await response.json();
        orderListElement.innerHTML = "";

        if (orders.length === 0) {
            orderListElement.innerHTML = "<p>Список заказов пуст</p>";
            orderListElement.classList.add("empty"); // Добавляем класс для центрирования
        } else {
            orderListElement.classList.remove("empty");
            orders.forEach(order => {
                const orderItem = document.createElement("div");
                orderItem.classList.add("order-item");

                const orderInfo = document.createElement("span");
                orderInfo.textContent = `Столик ${order.table}: ${order.dish}`;
                // Если заказ выполнен, добавляем визуальную индикацию
                if (order.completed) {
                    orderInfo.style.textDecoration = "line-through"; // Зачёркиваем выполненные заказы
                    orderInfo.style.color = "#888"; // Серый цвет для выполненных
                }

                const cookBtn = document.createElement("button");
                cookBtn.textContent = "Приготовить";
                cookBtn.disabled = order.completed; // Отключаем кнопку для выполненных заказов
                cookBtn.addEventListener("click", async () => {
                    try {
                        const response = await fetch('/api/cook_order', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ table: order.table, dish: order.dish })
                        });
                        const data = await response.json();
                        if (data.success) {
                            fetchOrders(); // Обновляем список заказов
                        } else {
                            alert(data.message || "Ошибка при приготовлении заказа");
                        }
                    } catch (error) {
                        console.error("Ошибка при приготовлении заказа:", error);
                    }
                });

                orderItem.appendChild(orderInfo);
                orderItem.appendChild(cookBtn);
                orderListElement.appendChild(orderItem);
            });
        }
    } catch (error) {
        console.error("Ошибка при получении списка заказов:", error);
    }
}