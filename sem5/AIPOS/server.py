import socket
import threading
import os
import time

class ImageServer:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.clients = {}
        self.images_dir = 'images'
        self.next_client_id = 1
        self.setup_images_dir()
        # словарь для отслеживания принадлежности файлов
        self.file_ownership = {} 
    

    def setup_images_dir(self):
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
            print(f"Создана директория {self.images_dir} для хранения изображений")
        else:
            print(f"Директория {self.images_dir} уже существует")
    

    def generate_client_id(self):
        client_id = str(self.next_client_id)
        self.next_client_id += 1
        return client_id
    

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        print(f"Сервер запущен на {self.host}:{self.port}")
        print("Ожидание подключений клиентов...")
        
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Подключен клиент: {client_address}")
            
            client_handler = threading.Thread(
                target=self.handle_client,
                args=(client_socket, client_address)
            )
            client_handler.daemon = True
            client_handler.start()
    

    def handle_client(self, client_socket, client_address):
        client_id = self.generate_client_id()
        self.clients[client_id] = (client_socket, client_address, time.time())
        
        print(f"Клиенту {client_address} присвоен ID: {client_id}")
        
        try:
            client_socket.send(f"YOUR_ID|{client_id}\n".encode('utf-8'))
            print(f"Отправлен ID клиенту {client_id}")
            
            # Уведомляем всех о новом клиенте
            self.broadcast_client_list()
            
            while True:
                try:
                    # Получаем команду от клиента
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break
                    
                    # Обрабатываем каждую команду отдельно
                    commands = data.strip().split('\n')
                    for command in commands:
                        if command.strip():
                            print(f"Получена команда от клиента {client_id}: {command}")
                            
                            if command == "LIST":
                                self.send_image_list(client_socket, client_id)  
                            elif command.startswith("SEND"):
                                self.receive_and_broadcast_image(client_socket, command, client_id)
                            elif command.startswith("DOWNLOAD"):
                                self.send_image_to_client(client_socket, command, client_id) 
                            elif command == "GET_CLIENTS":
                                self.send_client_list(client_socket)
                            elif command == "GET_ID":
                                client_socket.send(f"YOUR_ID|{client_id}\n".encode('utf-8'))
                    
                except Exception as e:
                    print(f"Ошибка при обработке команды от клиента {client_id}: {e}")
                    break
                    
        except Exception as e:
            print(f"Ошибка с клиентом {client_address}: {e}")
        finally:
            if client_id in self.clients:
                del self.clients[client_id]
            client_socket.close()
            print(f"Клиент {client_address} (ID: {client_id}) отключен")
            self.broadcast_client_list()


    def send_client_list(self, client_socket):
        try:
            clients_list = []
            for cid, (sock, addr, connect_time) in self.clients.items():
                clients_list.append(f"{cid}:{addr[0]}:{addr[1]}")
            
            message = "CLIENT_LIST|" + "|".join(clients_list) + "\n"
            print(f"Отправка списка клиентов: {message.strip()}")
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Ошибка при отправке списка клиентов: {e}")


    def broadcast_client_list(self):
        if not self.clients:
            return

        disconnected_clients = []
        for client_id, (client_socket, addr, connect_time) in self.clients.items():
            try:
                client_socket.getpeername()
            except:
                disconnected_clients.append(client_id)
        
        for client_id in disconnected_clients:
            if client_id in self.clients:
                del self.clients[client_id]
                print(f"Клиент {client_id} удален из списка")
        
        if not self.clients:
            return
        
        message_parts = []
        for cid, (sock, addr, connect_time) in self.clients.items():
            message_parts.append(f"{cid}:{addr[0]}:{addr[1]}")
        
        message = "CLIENT_LIST|" + "|".join(message_parts) + "\n"
        print(f"Broadcast списка клиентов: {message.strip()}")
        
        for client_id, (client_socket, addr, connect_time) in self.clients.items():
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                print(f"Не удалось отправить клиенту {client_id}")


    def send_image_list(self, client_socket, client_id):
        try:
            # показываем только файлы, предназначенные этому клиенту
            available_images = []
            for filename, (sender_id, recipient_id) in self.file_ownership.items():
                if recipient_id == client_id or sender_id == client_id:
                    available_images.append(filename)
            
            if not available_images:
                response = "NO_IMAGES\n"
                client_socket.send(response.encode('utf-8'))
            else:
                image_list = "|".join(available_images)
                response = f"IMAGES|{image_list}\n"
                client_socket.send(response.encode('utf-8'))
            
            print(f"Отправлен список изображений для клиента {client_id}: {response.strip()}")
        except Exception as e:
            print(f"Ошибка при отправке списка изображений: {e}")
            try:
                client_socket.send("ERROR\n".encode('utf-8'))
            except Exception as e:
                print(f"Не удалось отправить ошибку клиенту: {e}")


    def receive_and_broadcast_image(self, client_socket, command, sender_id):
        try:
            parts = command.split("|")
            if len(parts) >= 4:
                filename = parts[1]
                filesize = int(parts[2])
                recipient_id = parts[3]
                
                print(f"Получение файла {filename} размером {filesize} от {sender_id} для {recipient_id}")
                
                image_data = b""
                remaining = filesize
                
                while remaining > 0:
                    chunk = client_socket.recv(min(4096, remaining))
                    if not chunk:
                        break
                    image_data += chunk
                    remaining -= len(chunk)
                
                print(f"Файл {filename} полностью получен, размер: {len(image_data)} байт")
                
                # сохраняем информацию о принадлежности файла
                self.file_ownership[filename] = (sender_id, recipient_id)
                
                filepath = os.path.join(self.images_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                print(f"Файл {filename} сохранен на сервере")
                
                # уведомляем только отправителя и получателя
                client_socket.send("SEND_SUCCESS\n".encode('utf-8'))
                
                # Уведомляем получателя о новом изображении
                if recipient_id in self.clients:
                    recipient_socket, addr, connect_time = self.clients[recipient_id]
                    try:
                        recipient_socket.send(f"NEW_IMAGE|{filename}|{sender_id}\n".encode('utf-8'))
                        print(f"Уведомлен получатель {recipient_id} о новом файле {filename}")
                    except:
                        print(f"Не удалось уведомить получателя {recipient_id}")
                
                print(f"Файл {filename} успешно обработан")
                
        except Exception as e:
            print(f"Ошибка при получении изображения: {e}")
            try:
                client_socket.send("SEND_ERROR\n".encode('utf-8'))
            except Exception as e:
                print(f"Не удалось отправить ошибку клиенту: {e}")


    def send_image_to_client(self, client_socket, command, requesting_client_id):
        try:
            filename = command.split("|")[1]
            filepath = os.path.join(self.images_dir, filename)
            
            print(f"Запрос на скачивание файла: {filename} от клиента {requesting_client_id}")
            
            # проверяем права доступа
            if filename in self.file_ownership:
                sender_id, recipient_id = self.file_ownership[filename]
                if requesting_client_id != sender_id and requesting_client_id != recipient_id:
                    print(f"Клиент {requesting_client_id} не имеет прав на файл {filename}")
                    client_socket.send("ACCESS_DENIED\n".encode('utf-8'))
                    return
            
            if os.path.exists(filepath):
                filesize = os.path.getsize(filepath)
                response = f"FILE_INFO|{filename}|{filesize}\n"
                client_socket.send(response.encode('utf-8'))
                print(f"Отправлена информация о файле: {response.strip()}")
                
                ack = client_socket.recv(1024).decode('utf-8').strip()
                if ack == "READY":
                    print(f"Начинаем отправку файла {filename}")
                    with open(filepath, 'rb') as f:
                        sent_total = 0
                        while True:
                            chunk = f.read(4096)
                            if not chunk:
                                break
                            client_socket.send(chunk)
                            sent_total += len(chunk)
                    
                    print(f"Файл {filename} отправлен полностью, {sent_total} байт")
                else:
                    print(f"Неверное подтверждение от клиента: {ack}")
            else:
                print(f"Файл {filename} не найден")
                client_socket.send("FILE_NOT_FOUND\n".encode('utf-8'))
                
        except Exception as e:
            print(f"Ошибка при отправке изображения: {e}")
            try:
                client_socket.send("DOWNLOAD_ERROR\n".encode('utf-8'))
            except Exception as e:
                print(f"Не удалось отправить ошибку клиенту: {e}")

if __name__ == "__main__":
    server = ImageServer()
    server.start_server()
