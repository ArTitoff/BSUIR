// Отображение списка сотрудников
async function fetchEmployees() {
    try {
        const response = await fetch('/api/employees');
        const hiredEmployees = await response.json();

        employeeListElement.innerHTML = "";

        availableEmployees.forEach(employee => {
            const employeeItem = document.createElement("div");
            employeeItem.classList.add("employee-item");

            const employeeName = document.createElement("span");
            employeeName.textContent = employee.hired ? employee.name : `${employee.name} - ${employee.cost} руб.`;

            if (hiredEmployees.includes(employee.name) || employee.hired) {
                employee.hired = true;
                const checkMark = document.createElement("div");
                checkMark.classList.add("hired-check");
                checkMark.textContent = "✓";
                employeeItem.appendChild(employeeName);
                employeeItem.appendChild(checkMark);
            } else {
                const hireBtn = document.createElement("button");
                hireBtn.textContent = "Нанять";
                hireBtn.addEventListener("click", async () => {
                    try {
                        const response = await fetch('/api/hire_employee', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ name: employee.name, cost: employee.cost })
                        });
                        const data = await response.json();
                        if (data.success) {
                            employee.hired = true;
                            fetchEmployees();
                            fetchGameState();
                        } else {
                            alert(data.message || "Ошибка при найме сотрудника");
                        }
                    } catch (error) {
                        console.error("Ошибка при найме сотрудника:", error);
                    }
                });
                employeeItem.appendChild(employeeName);
                employeeItem.appendChild(hireBtn);
            }

            employeeListElement.appendChild(employeeItem);
        });
    } catch (error) {
        console.error("Ошибка при получении списка сотрудников:", error);
    }
}