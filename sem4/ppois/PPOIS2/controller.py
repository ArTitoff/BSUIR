import xml.dom.minidom as minidom
import xml.sax
import sqlite3
import re
import os
import logging
from model import Client, RecordModel

class Controller:
    def __init__(self, model: RecordModel, view):
        self.model = model
        self.view = view

    def set_view(self, view):
        self.view = view

    def add_client(self, name, surname, otchestvo, account_num, address, mob_telephone, home_telephone):
        client = Client(name, surname, otchestvo, account_num, address, mob_telephone, home_telephone)
        self.model.add_client(client)
        self.view.update_treeview()
        self.view.update_hierarchical_tree()

    def get_clients(self):
        return self.model.get_clients()

    def search_clients_by_first(self, query):
        return self.model.find_clients_by_phone_or_surname(phone=query, surname=query)
    
    def search_clients_by_second(self, query):
        return self.model.find_clients_by_account_or_address(account_num=int(query), address=query)

    def search_clients_by_third(self, query_2, query_1, query_3, query_4):
        return self.model.find_clients_by_fio_or_digits(name=query_2, surname=query_1, otchestvo=query_3, digits=query_4)
    
    def delete_clients_first(self, query):
        deleted_count = self.model.delete_clients_by_phone_or_surname(phone=query, surname=query)
        self.view.update_treeview()
        self.view.update_hierarchical_tree()
        return deleted_count
    
    def delete_clients_second(self, query):
        deleted_count = self.model.delete_clients_by_account_or_address(account_num=int(query), address=query)
        self.view.update_treeview()
        self.view.update_hierarchical_tree()
        return deleted_count
    
    def delete_clients_third(self, query_2, query_1, query_3, query_4):
        deleted_count = self.model.delete_clients_by_fio_or_digits(name=query_2, surname=query_1, otchestvo=query_3, digits=query_4)
        self.view.update_treeview()
        self.view.update_hierarchical_tree()
        return deleted_count

    def save_to_xml(self, file_path):
        doc = minidom.Document()
        root = doc.createElement("clients")
        doc.appendChild(root)

        for client in self.model.clients:
            client_element = doc.createElement("client")
            root.appendChild(client_element)

            name = doc.createElement("name")
            name.appendChild(doc.createTextNode(client.get_name()))
            client_element.appendChild(name)

            surname = doc.createElement("surname")
            surname.appendChild(doc.createTextNode(client.get_surname()))
            client_element.appendChild(surname)

            otchestvo = doc.createElement("otchestvo")
            otchestvo.appendChild(doc.createTextNode(client.get_otchestvo()))
            client_element.appendChild(otchestvo)

            account_num = doc.createElement("account_num")
            account_num.appendChild(doc.createTextNode(str(client.get_account_num())))
            client_element.appendChild(account_num)

            address = doc.createElement("address")
            address.appendChild(doc.createTextNode(client.get_address()))
            client_element.appendChild(address)

            mob_telephone = doc.createElement("mob_telephone")
            mob_telephone.appendChild(doc.createTextNode(client.get_mob_telephone()))
            client_element.appendChild(mob_telephone)

            home_telephone = doc.createElement("home_telephone")
            home_telephone.appendChild(doc.createTextNode(client.get_home_telephone()))
            client_element.appendChild(home_telephone)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(doc.toprettyxml(indent="  "))

    def load_from_xml(self, file_path):
        class ClientsHandler(xml.sax.ContentHandler):
            def __init__(self, model):
                self.model = model
                self.current_client = {}
                self.current_element = ""
                self.error_occurred = False
                self.error_messages = []
                self.success_count = 0

            def startElement(self, name, attrs):
                self.current_element = name

            def characters(self, content):
                if self.current_element and content.strip():
                    self.current_client[self.current_element] = content.strip()

            def endElement(self, name):
                if name == "client":
                    try:
                        # Получаем данные из XML
                        name = self.current_client.get("name", "")
                        surname = self.current_client.get("surname", "")
                        otchestvo = self.current_client.get("otchestvo", "")
                        account_num = self.current_client.get("account_num", "")
                        address = self.current_client.get("address", "")
                        mob_telephone = self.current_client.get("mob_telephone", "")
                        home_telephone = self.current_client.get("home_telephone", "")

                        # Валидация данных
                        if not name or not surname or not otchestvo or not address:
                             raise ValueError("Некорректный ввод", "Все поля должны быть заполнены")
                        if not re.match(r"^\+\d{7}$", mob_telephone):
                            raise ValueError("Мобильный телефон должен быть в формате +xxxxxxx")

                        if not re.match(r"^\d{3}-\d{3}$", home_telephone):
                            raise ValueError("Домашний телефон должен быть в формате xxx-xxx")

                        if not re.match(r"^\d{6}$", account_num):
                            raise ValueError("Номер счета должен быть в формате xxxxxx")

                        account_num = int(account_num)

                        # Создаем объект Client и добавляем в модель
                        client = Client(name, surname, otchestvo, account_num, address, mob_telephone, home_telephone)
                        self.model.add_client(client)
                        self.success_count += 1

                    except ValueError as e:
                        self.error_occurred = True
                        self.error_messages.append(f"Ошибка при обработке записи: {e}")
                    except Exception as e:
                        self.error_occurred = True
                        self.error_messages.append(f"Неизвестная ошибка при обработке записи: {e}")
                    finally:
                        self.current_client = {}

        handler = ClientsHandler(self.model)
        parser = xml.sax.make_parser()

        try:
            parser.setContentHandler(handler)
            parser.parse(file_path)
            
            if handler.error_occurred:
                message = f"Успешно загружено {handler.success_count} записей\n"
                message += "Ошибки при загрузке:\n" + "\n".join(handler.error_messages[:5])  # Ограничиваем количество сообщений
                return False, message
            return True, f"Успешно загружено {handler.success_count} записей"
            
        except xml.sax.SAXParseException as e:
            return False, f"Ошибка при чтении XML-файла: {e}"
        except Exception as e:
            return False, f"Неизвестная ошибка: {e}"

    def save_to_db(self, file_path):
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                name TEXT,
                surname TEXT,
                otchestvo TEXT,
                account_num INTEGER,
                address TEXT,
                mob_telephone TEXT,
                home_telephone TEXT
            )
        """)
        cursor.executemany(
            "INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?)",
            [(client.get_name(), client.get_surname(), client.get_otchestvo(), client.get_account_num(),
              client.get_address(), client.get_mob_telephone(), client.get_home_telephone())
             for client in self.model.clients]
        )
        conn.commit()
        conn.close()

    def load_from_db(self, file_path):
        try:
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clients'")
            if not cursor.fetchone():
                return False, "Таблица 'clients' не найдена в базе данных"

            cursor.execute("SELECT * FROM clients")
            rows = cursor.fetchall()

            if not rows:
                return False, "В базе данных нет записей"

            error_messages = []
            success_count = 0

            for row in rows:
                try:
                    name, surname, otchestvo, account_num, address, mob_telephone, home_telephone = row

                    if not name or not surname or not otchestvo or not address:
                        raise ValueError("Некорректный ввод", "Все поля должны быть заполнены")

                    if not re.match(r"^\+\d{7}$", mob_telephone):
                        raise ValueError("Мобильный телефон должен быть в формате +xxxxxxx")

                    if not re.match(r"^\d{3}-\d{3}$", home_telephone):
                        raise ValueError("Домашний телефон должен быть в формате xxx-xxx")

                    if not re.match(r"^\d{6}$", str(account_num)):
                        raise ValueError("Номер счета должен быть в формате xxxxxx")

                    account_num = int(account_num)

                    client = Client(name, surname, otchestvo, account_num, address, mob_telephone, home_telephone)
                    self.model.add_client(client)
                    success_count += 1

                except ValueError as e:
                    error_messages.append(f"Ошибка при обработке записи: {e}")
                except Exception as e:
                    error_messages.append(f"Неизвестная ошибка при обработке записи: {e}")

            if error_messages:
                return False, "\n".join(error_messages[:5])  # Ограничиваем количество сообщений
            
            return True, f"Успешно загружено {success_count} записей"

        except sqlite3.Error as e:
            return False, f"Ошибка при работе с базой данных: {e}"
        except Exception as e:
            return False, f"Неизвестная ошибка: {e}"
        finally:
            # Закрытие соединения с базой данных
            if 'conn' in locals() and conn:
                conn.close()
