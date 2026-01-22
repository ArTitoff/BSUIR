async function fetchTables() {
    try {
        const tableListElement = document.getElementById("tableList");
        console.log("fetchTables called");
        const response = await fetch('/api/tables');
        const tables = await response.json();
        tableListElement.innerHTML = "";

        // Отображаем все столы из полученного списка
        tables.forEach((table, index) => {
            const tableItem = document.createElement("div");
            tableItem.classList.add("table-item");

            const tableName = document.createElement("span");
            tableName.textContent = table.name;
            // Добавляем визуальную индикацию занятости
            tableName.style.color = table.occupied ? "red" : "green";

            const serveBtn = document.createElement("button");
            serveBtn.textContent = "Обслужить";
            serveBtn.disabled = !table.occupied; // Кнопка активна только для занятых столов
            serveBtn.addEventListener("click", async () => {
                try {
                    const response = await fetch('/api/issue_order', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ table: index + 1 })
                    });
                    const data = await response.json();
                    if (data.success) {
                        alert(`Стол ${index + 1} обслужен!`);
                        fetchTables(); // Обновляем список столов
                        fetchGameState();
                    } else {
                        alert(data.message || "Ошибка при обслуживании стола");
                    }
                } catch (error) {
                    console.error("Ошибка при обслуживании стола:", error);
                }
            });

            tableItem.appendChild(tableName);
            tableItem.appendChild(serveBtn);
            tableListElement.appendChild(tableItem);
        });
    } catch (error) {
        console.error("Ошибка при получении списка столов:", error);
    }
}