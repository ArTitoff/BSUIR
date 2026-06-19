import psycopg2
from datetime import datetime


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="postgres", 
            user="postgres", 
            password="asd123", 
            host="127.0.0.1", 
            port="5432"
        )
        self.create_tables()


    def create_tables(self):
        try:
            with self.conn.cursor() as cur:
                with open('/home/artem/Рабочий стол/BSUIR/PBZ/SQL_PBZ.sql', 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                
                cur.execute(sql_script)
                self.conn.commit()
                print("SQL файл выполнен")
                
        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка: {e}")
    

    # Методы для работы с владельцами
    def add_owner(self, license_number, full_name, address, birth_year, gender):
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL add_owner(%s, %s, %s, %s, %s)", 
                           (license_number, full_name, address, birth_year, gender))
                self.conn.commit()
                return True, "Владелец успешно добавлен"
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            error_msg = str(e)
            if "уже существует" in error_msg:
                return False, "Владелец с таким номером удостоверения уже существует"
            elif "birth_year" in error_msg:
                return False, "Некорректный год рождения (должен быть > 1920 и возраст >= 18 лет)"
            else:
                return False, f"Ошибка при добавлении владельца: {error_msg}"


    def get_owners(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM owners ORDER BY full_name")
            return cur.fetchall()


    def update_owner(self, license_number, full_name, address, birth_year, gender):
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL update_owner(%s, %s, %s, %s, %s)", 
                           (license_number, full_name, address, birth_year, gender))
                self.conn.commit()
                return True, "Владелец успешно обновлен"
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            return False, f"Ошибка при обновлении владельца: {str(e)}"


    def delete_owner(self, license_number):
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL delete_owner(%s)", (license_number,))
                self.conn.commit()
                return True, "Владелец успешно удален"
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            return False, f"Ошибка при удалении владельца: {str(e)}"


    # Метод для работы с двигателями
    def add_engine(self, engine_number, country, performance):
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL add_engine(%s, %s, %s)", 
                           (engine_number, country, performance))
                self.conn.commit()
                return True, "Двигатель успешно добавлен"
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            error_msg = str(e)
            if "уже существует" in error_msg:
                return False, "Двигатель с таким номером уже существует"
            else:
                return False, f"Ошибка при добавлении двигателя: {error_msg}"


    # Методы для работы с автомобилями
    def add_car(self, tech_passport_number, license_plate, engine_number, color, brand, owner_license_number, country, performance):
        try:
            with self.conn.cursor() as cur:
                # Сначала добавляем двигатель через процедуру
                engine_success, engine_message = self.add_engine(engine_number, country, performance)
                if not engine_success and "уже существует" not in engine_message:
                    return False, engine_message
                
                # Затем добавляем автомобиль через процедуру
                cur.execute("CALL add_car(%s, %s, %s, %s, %s, %s)", 
                           (tech_passport_number, license_plate, engine_number, color, brand, owner_license_number))
                self.conn.commit()
                return True, "Автомобиль успешно добавлен"
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            error_msg = str(e)
            if "уже существует" in error_msg:
                if "техпаспортом" in error_msg:
                    return False, "Автомобиль с таким техпаспортом уже существует"
                elif "номером" in error_msg:
                    return False, "Автомобиль с таким госномером уже существует"
            elif "Двигатель с номером" in error_msg:
                return False, "Двигатель с указанным номером не существует"
            elif "Владелец с номером" in error_msg:
                return False, "Владелец с указанным номером удостоверения не существует"
            else:
                return False, f"Ошибка при добавлении автомобиля: {error_msg}"


    def get_cars(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.*, e.country, e.performance, o.full_name 
                FROM cars c 
                LEFT JOIN engines e ON c.engine_number = e.engine_number
                LEFT JOIN owners o ON c.owner_license_number = o.license_number 
                ORDER BY c.license_plate
            """)
            return cur.fetchall()


    def update_car(self, tech_passport_number, license_plate, engine_number, color, brand, owner_license_number, country, performance):
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL update_car_with_engine(%s, %s, %s, %s, %s, %s, %s, %s)", 
                           (tech_passport_number, license_plate, color, brand, owner_license_number, 
                            engine_number, country, performance))
                self.conn.commit()
                return True, "Автомобиль успешно обновлен"
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            return False, f"Ошибка при обновлении автомобиля: {str(e)}"


    def delete_car(self, tech_passport_number):
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL delete_car(%s)", (tech_passport_number,))
                self.conn.commit()
                return True, "Автомобиль успешно удален"
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            return False, f"Ошибка при удалении автомобиля: {str(e)}"


    # Методы для работы с сотрудниками (используем процедуры)
    def add_inspector(self, full_name, position, rank):
        try:
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO inspectors (full_name, insp_position, insp_rank) VALUES (%s, %s, %s)", 
                           (full_name, position, rank))
                self.conn.commit()
                return True, "Сотрудник успешно добавлен"
        except Exception as e:
            self.conn.rollback()
            return False, f"Ошибка при добавлении сотрудника: {str(e)}"


    def get_inspectors(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM inspectors ORDER BY full_name")
            return cur.fetchall()


    def update_inspector(self, inspector_id, full_name, position, rank):
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL update_inspector(%s, %s, %s, %s)", 
                           (inspector_id, full_name, position, rank))
                self.conn.commit()
                return True, "Сотрудник успешно обновлен"
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            return False, f"Ошибка при обновлении сотрудника: {str(e)}"


    def delete_inspector(self, inspector_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL delete_inspector(%s)", (inspector_id,))
                self.conn.commit()
                return True, "Сотрудник успешно удален"
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            return False, f"Ошибка при удалении сотрудника: {str(e)}"


    # Методы для работы с осмотрами 
    def add_inspection(self, car_license_plate, inspector_id, inspection_date, result, conclusion):
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL add_inspection(%s, %s, %s, %s, %s)", 
                           (car_license_plate, inspector_id, inspection_date, result, conclusion))
                self.conn.commit()
                return True, "Осмотр успешно добавлен"
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            error_msg = str(e)
            if "не может иметь больше 10 осмотров" in error_msg:
                return False, "Сотрудник не может проводить более 10 осмотров в день"
            elif "Автомобиль с номером" in error_msg:
                return False, "Автомобиль с указанным госномером не существует"
            elif "Инспектор с id" in error_msg:
                return False, "Инспектор с указанным ID не существует"
            else:
                return False, f"Ошибка при добавлении осмотра: {error_msg}"


    def get_inspections(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT i.*, c.brand, c.color, c.engine_number, ins.full_name, ins.insp_rank
                FROM inspections i
                JOIN cars c ON i.car_license_plate = c.license_plate
                JOIN inspectors ins ON i.inspector_id = ins.id
                ORDER BY i.inspection_date DESC
            """)
            return cur.fetchall()


    def update_inspection(self, inspection_id, car_license_plate, inspector_id, inspection_date, result, conclusion):
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL update_inspection(%s, %s, %s, %s, %s, %s)", 
                           (inspection_id, car_license_plate, inspector_id, inspection_date, result, conclusion))
                self.conn.commit()
                return True, "Осмотр успешно обновлен"
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            return False, f"Ошибка при обновлении осмотра: {str(e)}"


    def delete_inspection(self, inspection_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL delete_inspection(%s)", (inspection_id,))
                self.conn.commit()
                return True, "Осмотр успешно удален"
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            return False, f"Ошибка при удалении осмотра: {str(e)}"


    # Отчеты 
    def get_inspections_by_period(self, start_date, end_date):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT inspection_date, COUNT(*) as count
                FROM inspections
                WHERE inspection_date BETWEEN %s AND %s
                GROUP BY inspection_date
                ORDER BY inspection_date
            """, (start_date, end_date))
            return cur.fetchall()

            
    def get_inspectors_by_date(self, date):
        with self.conn.cursor() as cur:
            try:
                cur.execute("""
                    SELECT ins.full_name, ins.insp_rank, array_agg(DISTINCT i.car_license_plate) as cars
                    FROM inspectors ins
                    JOIN inspections i ON ins.id = i.inspector_id
                    WHERE i.inspection_date = %s
                    GROUP BY ins.id, ins.full_name, ins.insp_rank
                """, (date,))
                result = cur.fetchall()
                return result if result else []
            except psycopg2.DatabaseError as e:
                self.conn.rollback()
                print(f"Ошибка при получении сотрудников по дате: {str(e)}")
                return []
        

    def get_car_history(self, engine_number):
        with self.conn.cursor() as cur:
            try:
                # Используем функцию
                cur.execute("SELECT * FROM check_inspections_hystory_by_engine(%s)", (engine_number,))
                return cur.fetchall()
            except psycopg2.DatabaseError:
                self.conn.rollback()
                return []