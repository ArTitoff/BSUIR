from core.catalog import Catalog
from core.cashbox import Cashbox
from core.customer import Customer
from core.consultant import Consultant
from core.electroshop import Electroshop
from core.share import Share
from core.product import Product
import json
from typing import Optional, List



class Init:
    def __init__(self):
        self.catalog = Catalog()
        self.electroshop = Electroshop()
        self.load_state()

        if not self.catalog.get_catalog():
            self.initialize_catalog()
        
        self.consultant = Consultant()

    def initialize_catalog(self):
        self.catalog.add_product("Iphone 15 pro", 4000, 1)
        self.catalog.add_product("Пылесос Sumsung 2374", 1745, 2)
        self.catalog.add_product("Холодильник Атлант", 2740, 5)
        self.catalog.add_product("Xiaomi", 1350, 2)
        self.catalog.add_product("Notebook Lenovo", 2840, 5)
        self.catalog.add_product("Душесос 3000", 9999, 0)
        self.catalog.add_product("Семантический компьютер", 777, 30)

        list1 = [self.catalog.find_product("Iphone 15 pro"), self.catalog.find_product("Xiaomi")]
        list2 = [self.catalog.find_product("Душесос 3000"), self.catalog.find_product("Холодильник Атлант")]
        list3 = [self.catalog.find_product("Семантический компьютер")]

        self.electroshop.add_customer("Bob", 7000, list1)
        self.electroshop.add_customer("Lesli", 2000, list2)
        self.electroshop.add_customer("Jessika", 30, list3)

    def load_state(self) -> None:
        try:
            with open('state.json', 'r') as f:
                data = json.load(f)
                
                if 'products' in data and isinstance(data['products'], list):
                    for product in data['products']:
                        if all(key in product for key in ['name', 'price', 'guarantee']):
                            self.catalog.add_product(product['name'], product['price'], product['guarantee'])
                        else:
                            print("Пропущен продукт из-за отсутствия необходимых полей.")
                else:
                    print("Нет данных о продуктах.")

                if 'customers' in data and isinstance(data['customers'], list):
                    for customer in data['customers']:
                        if all(key in customer for key in ['name', 'money', 'purchases']):
                            purchases = [self.catalog.find_product(p) for p in customer['purchases']]
                            self.update_customer(customer['name'], customer['money'], purchases)
                        else:
                            print("Пропущен клиент из-за отсутствия необходимых полей.")
                else:
                    print("Нет данных о клиентах.")

        except FileNotFoundError:
            print("Файл состояния не найден, начинается новая сессия.")
        except json.JSONDecodeError:
            print("Ошибка при чтении файла состояния. Файл может быть поврежден.")

    def save_state(self) -> None:
        data = {
            'products': [
                {
                    'name': p.get_name(),
                    'price': p.get_price(),
                    'guarantee': p.get_guarantee()
                } for p in self.catalog.get_catalog()
            ],
            'customers': [
                {
                    'name': c.get_name(),
                    'money': c.get_money(),
                    'purchases': [p.get_name() for p in c.get_customer_products() if p is not None]
                }
                for c in self.electroshop.get_customers() if c is not None
            ]
        }
        
        with open('state.json', 'w') as f:
            json.dump(data, f)

    def update_customer(self, name: str, money: int, purchases: List[Product]) -> None:
        customer_found = False
        
        for customer in self.electroshop.get_customers():
            if customer.get_name() == name:
                customer_found = True
                customer.set_money(money)  
                customer.set_customer_products(purchases)
                break
        
        if not customer_found:
            self.electroshop.add_customer(name, money, purchases)

    def display_menu(self) -> None:
        print("\nМеню:")
        print("1. Поиск товара в каталоге")
        print("2. Часто задаваемые вопросы")
        print("3. Купить товар")
        print("4. Вернуть товар")
        print("5. Участвовать в акции")
        print("6. Выход\n")

    def find_product_by_name(self) -> Optional[Product]:
        name: str = input("Введите название продукта: ")
        product: Optional[Product] = self.catalog.find_product(name)
        
        if product:
            product.print_info()
            return product
        else:
            print("Такого у нас нет")
            return None

    def buy_product_by_customer(self) -> None:
        self.electroshop.show_customers()
        customer: Customer = self.electroshop.get_customer()
        self.catalog.display_catalog()
        product: Optional[Product] = self.find_product_by_name()
        
        if not product:
            print("Всё заново")
            return
        
        Cashbox.buy_product(customer, product)

    def return_product_by_customer(self) -> None:
        self.electroshop.show_customers()
        customer: Customer = self.electroshop.get_customer()
        customer.print_info()
        product: Optional[Product] = self.find_product_by_name()
        
        if not product:
            print("Всё заново")
            return
        
        Cashbox.return_product(customer, product)

    def customer_lottery(self) -> None:
        self.electroshop.show_customers()
        customer: Customer = self.electroshop.get_customer()
        
        if Share.lottery():
            print("Вы выиграли 20 BYN!!!! ")
            money: int = customer.get_money()
            new_balance: int = money + 20
            customer.set_money(new_balance)
        else:
            print("Вы проиграли :(")

    def main_menu(self) -> None:
        while True:
            self.display_menu()

            try:
                choice: int = int(input("Выберите действие (1-6): "))
                if choice == 1:
                    self.find_product_by_name()
                elif choice == 2:
                    self.consultant.show_questions()
                    self.consultant.choice_question()
                elif choice == 3:
                    self.buy_product_by_customer()
                elif choice == 4:
                    self.return_product_by_customer()
                elif choice == 5:
                    self.customer_lottery()
                elif choice == 6:
                    print("Выход из программы.")
                    self.save_state() 
                    break
                else:
                    print("Введите верное число от 1 до 6")
            except ValueError:
                print("Введите верное число от 1 до 6")

if __name__ == "__main__":
    app = Init()
    app.main_menu()