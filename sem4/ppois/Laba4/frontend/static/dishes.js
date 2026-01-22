// Получение и отображение списка блюд
async function fetchDishes() {
    try {
        const response = await fetch('/api/dishes');
        const dishes = await response.json();
        dishListElement.innerHTML = "";

        if (dishes.length === 0) {
            dishListElement.innerHTML = "<p>Список блюд пуст</p>";
            document.getElementById("dishList").style.textAlign = "center";
        } else {
            dishes.forEach(dish => {
                const dishItem = document.createElement("div");
                dishItem.classList.add("dish-item");

                const dishName = document.createElement("span");
                dishName.textContent = dish;

                const removeBtn = document.createElement("button");
                removeBtn.textContent = "Удалить";
                removeBtn.addEventListener("click", async () => {
                    try {
                        const response = await fetch('/api/remove_dish', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ name: dish })
                        });
                        const data = await response.json();
                        if (data.success) {
                            fetchDishes();
                        } else {
                            alert("Ошибка при удалении блюда");
                        }
                    } catch (error) {
                        console.error("Ошибка при удалении блюда:", error);
                    }
                });

                dishItem.appendChild(dishName);
                dishItem.appendChild(removeBtn);
                dishListElement.appendChild(dishItem);
            });
        }
    } catch (error) {
        console.error("Ошибка при получении списка блюд:", error);
    }
}

// Добавление блюда
function addDishHandler() {
    const dishName = dishInput.value.trim();
    if (dishName) {
        fetch('/api/add_dish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: dishName })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    dishInput.value = "";
                    addDishPanel.classList.add("hidden");
                    fetchDishes();
                } else {
                    alert("Ошибка при добавлении блюда");
                }
            })
            .catch(error => console.error("Ошибка при добавлении блюда:", error));
    } else {
        alert("Введите название блюда");
    }
}