document.getElementById("startGame").addEventListener("click", () => startPanel.classList.remove("hidden"));
document.getElementById("menu").addEventListener("click", () => {
    menuPanel.classList.remove("hidden");
    fetchDishes();
});
document.getElementById("hall").addEventListener("click", () => {
    hallPanel.classList.remove("hidden");
    fetchTables();
});
document.getElementById("orders").addEventListener("click", () => {
    document.getElementById("orderPanel").classList.remove("hidden");
    fetchOrders();
});
document.getElementById("employee").addEventListener("click", () => {
    employeePanel.classList.remove("hidden");
    fetchEmployees();
});

// Закрытие панелей
document.getElementById("closeStartPanel").addEventListener("click", () => startPanel.classList.add("hidden"));
document.getElementById("closeMenuPanel").addEventListener("click", () => menuPanel.classList.add("hidden"));
document.getElementById("closeHallPanel").addEventListener("click", () => hallPanel.classList.add("hidden"));
document.getElementById("closeOrderPanel").addEventListener("click", () => orderPanel.classList.add("hidden"));
document.getElementById("closeEmployeePanel").addEventListener("click", () => employeePanel.classList.add("hidden"));
document.getElementById("closeAddDishPanel").addEventListener("click", () => addDishPanel.classList.add("hidden"));

// Отрытие панелей
addDishBtn.addEventListener("click", () => addDishPanel.classList.remove("hidden"));
submitDishBtn.addEventListener("click", addDishHandler);
startBtn.addEventListener("click", startGame);
takeOrderBtn.addEventListener("click", takeOrder);
cookBtn.addEventListener("click", cookFood);
serveBtn.addEventListener("click", serveFood);

// Инициализация состояния игры при загрузке
fetchGameState();