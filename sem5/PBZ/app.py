from flask import Flask, render_template, request, redirect, url_for, flash
from database import Database
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
db = Database()

# Получаем текущую дату и год
current_year = datetime.now().year
current_date = datetime.now().strftime('%Y-%m-%d')

@app.route('/')
def index():
    return render_template('base.html')

# Владельцы
@app.route('/owners')
def owners():
    owners_list = db.get_owners()
    return render_template('owners.html', 
                         owners=owners_list, 
                         current_year=current_year)

@app.route('/add_owner', methods=['POST'])
def add_owner():
    license_number = request.form['license_number']
    full_name = request.form['full_name']
    address = request.form['address']
    birth_year = int(request.form['birth_year'])
    gender = request.form['gender']
    
    success, message = db.add_owner(license_number, full_name, address, birth_year, gender)  
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('owners'))

@app.route('/edit_owner', methods=['POST'])
def edit_owner():
    license_number = request.form['license_number']
    full_name = request.form['full_name']
    address = request.form['address']
    birth_year = int(request.form['birth_year'])
    gender = request.form['gender']
    
    success, message = db.update_owner(license_number, full_name, address, birth_year, gender)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('owners'))

@app.route('/delete_owner/<string:license_number>')
def delete_owner(license_number):
    success, message = db.delete_owner(license_number)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('owners'))

# Автомобили
@app.route('/cars')
def cars():
    cars_list = db.get_cars()
    owners_list = db.get_owners()
    return render_template('cars.html', 
                         cars=cars_list, 
                         owners=owners_list)

@app.route('/add_car', methods=['POST'])
def add_car():
    tech_passport_number = request.form['tech_passport_number']
    license_plate = request.form['license_plate']
    engine_number = request.form['engine_number']
    color = request.form['color']
    brand = request.form['brand']
    owner_license_number = request.form['owner_license_number']
    country = request.form['country']
    performance = int(request.form['performance'])
    
    success, message = db.add_car(tech_passport_number, license_plate, engine_number, color, brand, owner_license_number, country, performance)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('cars'))

@app.route('/edit_car', methods=['POST'])
def edit_car():
    tech_passport_number = request.form['tech_passport_number']
    license_plate = request.form['license_plate']
    engine_number = request.form['engine_number']
    color = request.form['color']
    brand = request.form['brand']
    owner_license_number = request.form['owner_license_number']
    country = request.form['country']
    performance = int(request.form['performance'])
    
    success, message = db.update_car(tech_passport_number, license_plate, engine_number, color, brand, owner_license_number, country, performance)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('cars'))

@app.route('/delete_car/<string:tech_passport_number>')
def delete_car(tech_passport_number):
    success, message = db.delete_car(tech_passport_number)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('cars'))

# Сотрудники
@app.route('/inspectors')
def inspectors():
    inspectors_list = db.get_inspectors()
    return render_template('inspectors.html', inspectors=inspectors_list)

@app.route('/add_inspector', methods=['POST'])
def add_inspector():
    full_name = request.form['full_name']
    position = request.form['position']
    rank = request.form['rank']
    
    success, message = db.add_inspector(full_name, position, rank)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('inspectors'))

@app.route('/edit_inspector', methods=['POST'])
def edit_inspector():
    inspector_id = int(request.form['inspector_id'])
    full_name = request.form['full_name']
    position = request.form['position']
    rank = request.form['rank']
    
    success, message = db.update_inspector(inspector_id, full_name, position, rank)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('inspectors'))

@app.route('/delete_inspector/<int:inspector_id>')
def delete_inspector(inspector_id):
    success, message = db.delete_inspector(inspector_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('inspectors'))

# Осмотры
@app.route('/inspections')
def inspections():
    inspections_list = db.get_inspections()
    cars_list = db.get_cars()
    inspectors_list = db.get_inspectors()
    return render_template('inspections.html', 
                         inspections=inspections_list, 
                         cars=cars_list, 
                         inspectors=inspectors_list,
                         current_date=current_date)

@app.route('/add_inspection', methods=['POST'])
def add_inspection():
    car_license_plate = request.form['car_license_plate']
    inspector_id = int(request.form['inspector_id'])
    inspection_date = request.form['inspection_date']
    result = request.form['result'] == 'true'
    conclusion = request.form['conclusion']
    
    success, message = db.add_inspection(car_license_plate, inspector_id, inspection_date, result, conclusion)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('inspections'))

@app.route('/edit_inspection', methods=['POST'])
def edit_inspection():
    inspection_id = int(request.form['inspection_id'])
    car_license_plate = request.form['car_license_plate']
    inspector_id = int(request.form['inspector_id'])
    inspection_date = request.form['inspection_date']
    result = request.form['result'] == 'true'
    conclusion = request.form['conclusion']
    
    success, message = db.update_inspection(inspection_id, car_license_plate, inspector_id, inspection_date, result, conclusion)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('inspections'))

@app.route('/delete_inspection/<int:inspection_id>')
def delete_inspection(inspection_id):
    success, message = db.delete_inspection(inspection_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('inspections'))

# Отчеты
@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/inspections_report', methods=['POST'])
def inspections_report():
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    report_data = db.get_inspections_by_period(start_date, end_date)
    return render_template('reports.html', 
                         report_data=report_data, 
                         start_date=start_date, 
                         end_date=end_date,
                         current_date=current_date)

@app.route('/inspectors_report', methods=['POST'])
def inspectors_report():
    date = request.form['date']
    report_data = db.get_inspectors_by_date(date)
    return render_template('reports.html', 
                         inspectors_data=report_data, 
                         date=date,
                         current_date=current_date)

@app.route('/car_history')
def car_history():
    engine_number = request.args.get('engine_number')
    history = []
    if engine_number:
        history = db.get_car_history(engine_number)
    return render_template('car_history.html', 
                         history=history, 
                         engine_number=engine_number)

if __name__ == '__main__':
    app.run(debug=True)