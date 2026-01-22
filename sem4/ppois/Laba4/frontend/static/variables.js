const cashElement = document.getElementById("cash");
const timeElement = document.getElementById("time");
const customersElement = document.getElementById("customers");

const startGameBtn = document.getElementById("startGame");
const takeOrderBtn = document.getElementById("takeOrder");
const cookBtn = document.getElementById("cook");
const serveBtn = document.getElementById("serve");

const startBtn = document.getElementById("start");
const addDishBtn = document.getElementById("addDish");
const submitDishBtn = document.getElementById("submitDish");

const startPanel = document.getElementById("startPanel");
const menuPanel = document.getElementById("menuPanel");
const hallPanel = document.getElementById("hallPanel");
const employeePanel = document.getElementById("employeePanel");
const orderPanel = document.getElementById("orderPanel");
const addDishPanel = document.getElementById("addDishPanel");

const dishListElement = document.getElementById("dishList");
const dishInput = document.getElementById("dishInput");
const employeeListElement = document.getElementById("employeeList");

const orderListElement = document.getElementById("orderList");

let gameActive = false;

const availableEmployees = [
    { name: "Аня", cost: 100, hired: false },
    { name: "Игорь", cost: 150, hired: false },
    { name: "Катя", cost: 200, hired: false }
];