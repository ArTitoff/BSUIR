import sys
from pathlib import Path

# Добавляем корень проекта в пути поиска модулей
sys.path.append(str(Path(__file__).parent.parent))  # Поднимаемся на уровень выше (из web/)

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from core.catalog import Catalog
from core.electroshop import Electroshop
from core.consultant import Consultant
from core.cashbox import Cashbox
from core.share import Share
import json
import os
import random  # Добавляем импорт random


app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Инициализация системы
def init_system():
    system = {
        'catalog': Catalog(),
        'electroshop': Electroshop(),
        'consultant': Consultant()
    }
    
    # Загрузка состояния
    if os.path.exists('state.json'):
        try:
            with open('state.json', 'r') as f:
                data = json.load(f)
                
                if 'products' in data:
                    for product in data['products']:
                        system['catalog'].add_product(
                            product['name'], 
                            product['price'], 
                            product['guarantee']
                        )
                
                if 'customers' in data:
                    for customer in data['customers']:
                        purchases = []
                        for p in customer['purchases']:
                            product = system['catalog'].find_product(p)
                            if product:
                                purchases.append(product)
                        system['electroshop'].add_customer(
                            customer['name'], 
                            customer['money'], 
                            purchases
                        )
        except Exception as e:
            print(f"Error loading state: {e}")
    
    return system

system = init_system()

# Сохранение состояния
def save_state():
    data = {
        'products': [
            {
                'name': p.get_name(),
                'price': p.get_price(),
                'guarantee': p.get_guarantee()
            } for p in system['catalog'].get_catalog()
        ],
        'customers': [
            {
                'name': c.get_name(),
                'money': c.get_money(),
                'purchases': [p.get_name() for p in c.get_customer_products()]
            }
            for c in system['electroshop'].get_customers()
        ]
    }
    
    with open('state.json', 'w') as f:
        json.dump(data, f)


# Маршруты
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/catalog')
def catalog():
    products = system['catalog'].get_catalog()
    return render_template('catalog.html', products=products)


@app.route('/customers')
def customers():
    customers = system['electroshop'].get_customers()
    return render_template('customers.html', customers=customers)


@app.route('/faq')
def faq():
    return render_template('faq.html', questions=system['consultant'].questions.items())


@app.route('/faq/<int:question_id>')
def faq_answer(question_id):
    answer = system['consultant'].get_answer(question_id)
    return render_template('faq_answer.html', 
                         question=system['consultant'].questions[question_id][0],
                         answer=answer)


@app.route('/buy', methods=['GET', 'POST'])
def buy_product():
    if request.method == 'POST':
        customer_name = request.form['customer']
        product_name = request.form['product']
        
        customer = next((c for c in system['electroshop'].get_customers() 
                        if c.get_name() == customer_name), None)
        product = system['catalog'].find_product(product_name)
        
        if customer and product:
            if customer.get_money() >= product.get_price():
                Cashbox.buy_product(customer, product)
                save_state()
                flash('Покупка успешно совершена!', 'success')
            else:
                flash('Недостаточно средств для покупки!', 'danger')
            return redirect(url_for('customers'))
    
    customers = system['electroshop'].get_customers()
    products = system['catalog'].get_catalog()
    return render_template('buy.html', customers=customers, products=products)


@app.route('/return', methods=['GET', 'POST'])
def return_product():
    if request.method == 'POST':
        customer_name = request.form['customer']
        product_name = request.form['product']
        
        customer = next((c for c in system['electroshop'].get_customers() 
                        if c.get_name() == customer_name), None)
        
        if customer:
            for product in customer.get_customer_products():
                if product.get_name().lower() == product_name.lower():
                    Cashbox.return_product(customer, product)
                    save_state()
                    flash('Товар успешно возвращен!', 'success')
                    return redirect(url_for('customers'))
            
            flash('Товар не найден!', 'danger')
    
    customers = system['electroshop'].get_customers()
    return render_template('return.html', customers=customers)


@app.route('/lottery', methods=['GET', 'POST'])
def lottery():
    if request.method == 'POST':
        customer_name = request.form['customer']
        customer = next((c for c in system['electroshop'].get_customers() 
                        if c.get_name() == customer_name), None)
        
        if customer:
            # Измененная логика лотереи для веб-интерфейса
            choice = random.randint(1, 5)
            random_number = random.randint(1, 5)
            if choice == random_number:
                customer.set_money(customer.get_money() + 20)
                save_state()
                return render_template('lottery_result.html', 
                                     result="Вы выиграли 20 BYN!!!!", 
                                     customer=customer)
            else:
                return render_template('lottery_result.html', 
                                     result="Вы проиграли :(", 
                                     customer=customer)
    
    customers = system['electroshop'].get_customers()
    return render_template('lottery.html', customers=customers)


if __name__ == '__main__':
    app.run(debug=True)