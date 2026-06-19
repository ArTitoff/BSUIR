import socket
import threading
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time


class ImageClient:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.socket = None
        self.client_id = None
        self.download_dir = 'downloads'
        self.connected_clients = {}
        self.setup_download_dir()
        self.listening = False
        

    def setup_download_dir(self):
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
    

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
            self.listening = True
            listen_thread = threading.Thread(target=self.listen_to_server)
            listen_thread.daemon = True
            listen_thread.start()
            
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False
    

    def listen_to_server(self):
        buffer = ""
        while self.listening:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    print("Соединение с сервером разорвано")
                    break
                    
                buffer += data
                lines = buffer.split('\n')
                buffer = lines[-1]
                
                for line in lines[:-1]:
                    if line.strip():
                        print(f"Получено сообщение от сервера: {line}")
                        try:
                            self.process_server_message(line.strip())
                        except Exception as e:
                            print(f"Ошибка при обработке сообщения '{line}': {e}")
                            
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Критическая ошибка при прослушивании сервера: {e}")
                break
        
        print("Поток прослушивания сервера завершен")
        self.listening = False
    

    def process_server_message(self, message):
        if message.startswith("YOUR_ID"):
            self.client_id = message.split("|")[1]
            print(f"Установлен ID клиента: {self.client_id}")
            if hasattr(self, 'gui'):
                self.gui.id_label.config(text=f"Ваш ID: {self.client_id}")
                self.gui.send_btn.config(state="normal")
                
        elif message.startswith("CLIENT_LIST"):
            clients_data = message.split("|")[1:]
            self.connected_clients.clear()
            for client_data in clients_data:
                if client_data:
                    parts = client_data.split(":")
                    if len(parts) >= 2:
                        client_id = parts[0]
                        client_addr = ":".join(parts[1:])
                        self.connected_clients[client_id] = client_addr
            
            if hasattr(self, 'gui'):
                self.gui.update_clients_list(self.connected_clients)
                
        elif message.startswith("IMAGES"):
            images = message.split("|")[1:]
            if hasattr(self, 'gui'):
                self.gui.update_image_list(images)
                
        elif message.startswith("NEW_IMAGE"):
            parts = message.split("|")
            if len(parts) >= 3:
                filename = parts[1]
                sender_id = parts[2]
                if hasattr(self, 'gui'):
                    self.get_image_list()
                    
        elif message == "NO_IMAGES":
            if hasattr(self, 'gui'):
                self.gui.update_image_list([])
                
        elif message == "SEND_SUCCESS":
            if hasattr(self, 'gui'):
                messagebox.showinfo("Успех", "Изображение успешно отправлено")
                
        elif message == "SEND_ERROR":
            if hasattr(self, 'gui'):
                messagebox.showerror("Ошибка", "Ошибка при отправке изображения")
                
        elif message.startswith("FILE_INFO"):
            parts = message.split("|")
            if len(parts) >= 3:
                filename = parts[1]
                filesize = int(parts[2])
                self.receive_image_file(filename, filesize)
    

    def receive_image_file(self, filename, filesize):
        try:
            self.socket.send("READY".encode('utf-8'))
            
            filepath = os.path.join(self.download_dir, filename)
            received_size = 0
            
            print(f"Начинаем прием файла {filename}, размер: {filesize} байт")
            
            with open(filepath, 'wb') as f:
                while received_size < filesize:
                    chunk = self.socket.recv(min(4096, filesize - received_size))
                    if not chunk:
                        break
                    f.write(chunk)
                    received_size += len(chunk)
            
            if received_size == filesize:
                print(f"Файл {filename} успешно сохранен в {filepath}")
                if hasattr(self, 'gui'):
                    messagebox.showinfo("Успех", f"Файл {filename} успешно скачан")
            else:
                print(f"Ошибка: получено {received_size} из {filesize} байт")
                if hasattr(self, 'gui'):
                    messagebox.showerror("Ошибка", f"Ошибка при скачивании {filename}")
                    
        except Exception as e:
            print(f"Ошибка при получении файла {filename}: {e}")
            if hasattr(self, 'gui'):
                messagebox.showerror("Ошибка", f"Ошибка при скачивании {filename}: {e}")
    

    def send_command(self, command):
        try:
            full_command = command + "\n"
            self.socket.send(full_command.encode('utf-8'))
            print(f"Отправлена команда: {command}")
            return True
        except Exception as e:
            print(f"Ошибка при отправке команды: {e}")
            return False
    

    def get_connected_clients(self):
        return self.send_command("GET_CLIENTS")
    

    def get_image_list(self):
        return self.send_command("LIST")
    

    def send_image(self, filepath, recipient_id):
        try:
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)
            
            command = f"SEND|{filename}|{filesize}|{recipient_id}"
            if not self.send_command(command):
                return "ERROR|Не удалось отправить команду"
            
            time.sleep(0.1)
            
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    self.socket.send(chunk)
            
            return "SEND_SUCCESS"
            
        except Exception as e:
            return f"ERROR|{e}"
    

    def download_image(self, filename):
        try:
            if not self.send_command(f"DOWNLOAD|{filename}"):
                return "ERROR|Не удалось отправить команду"
            return "SUCCESS|Файл запрошен"
        except Exception as e:
            return f"ERROR|{e}"
    

    def disconnect(self):
        self.listening = False
        if self.socket:
            self.socket.close()


class ClientGUI:
    def __init__(self):
        self.client = ImageClient()
        self.client.gui = self
        self.root = tk.Tk()
        self.root.title("Клиент для обмена изображениями")
        self.root.geometry("700x600")  
        self.setup_ui()
        

    def setup_ui(self):
        conn_frame = ttk.Frame(self.root, padding="10")
        conn_frame.grid(row=0, column=0, sticky="ew")
        
        self.id_label = ttk.Label(conn_frame, text="Ваш ID: не подключен", 
                                 foreground="blue", font=('Arial', 10, 'bold'))
        self.id_label.grid(row=0, column=0, sticky="w", columnspan=5)
        
        ttk.Label(conn_frame, text="Сервер:").grid(row=1, column=0)
        self.host_entry = ttk.Entry(conn_frame, width=15)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=1, column=1)
        
        ttk.Label(conn_frame, text="Порт:").grid(row=1, column=2)
        self.port_entry = ttk.Entry(conn_frame, width=8)
        self.port_entry.insert(0, "8888")
        self.port_entry.grid(row=1, column=3)
        
        self.connect_btn = ttk.Button(conn_frame, text="Подключиться", 
                                    command=self.connect_to_server)
        self.connect_btn.grid(row=1, column=4, padx=10)
        
        clients_frame = ttk.LabelFrame(self.root, text="Подключенные клиенты", padding="10")
        clients_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        self.clients_tree = ttk.Treeview(clients_frame, columns=("ID", "Address"), show="headings", height=4)
        self.clients_tree.heading("ID", text="ID клиента")
        self.clients_tree.heading("Address", text="Адрес")
        self.clients_tree.column("ID", width=150)
        self.clients_tree.column("Address", width=200)
        self.clients_tree.grid(row=0, column=0, sticky="ew")

        self.clients_tree.bind('<<TreeviewSelect>>', self.on_client_select)
        
        clients_scrollbar = ttk.Scrollbar(clients_frame, orient="vertical", 
                                        command=self.clients_tree.yview)
        clients_scrollbar.grid(row=0, column=1, sticky="ns")
        self.clients_tree.configure(yscrollcommand=clients_scrollbar.set)
        
        ttk.Button(clients_frame, text="Обновить список", 
                  command=self.refresh_clients).grid(row=1, column=0, pady=5)
        
        send_frame = ttk.LabelFrame(self.root, text="Отправка изображения", padding="10")
        send_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        self.file_label = ttk.Label(send_frame, text="Файл не выбран")
        self.file_label.grid(row=0, column=0, columnspan=3, sticky="w")
        
        ttk.Button(send_frame, text="Выбрать файл", 
                  command=self.select_file).grid(row=1, column=0, pady=5)
        
        ttk.Label(send_frame, text="ID получателя:").grid(row=1, column=1)
        self.recipient_entry = ttk.Entry(send_frame, width=15)
        self.recipient_entry.grid(row=1, column=2)
        
        ttk.Button(send_frame, text="Выбрать из списка", 
                  command=self.select_recipient_from_list).grid(row=1, column=3, padx=5)
        
        self.send_btn = ttk.Button(send_frame, text="Отправить", 
                                 command=self.send_image, state="disabled")
        self.send_btn.grid(row=1, column=4, padx=10)
        
        list_frame = ttk.LabelFrame(self.root, text="Доступные изображения", padding="10")
        list_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        
        self.image_listbox = tk.Listbox(list_frame, height=8)
        self.image_listbox.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", 
                                command=self.image_listbox.yview)
        scrollbar.grid(row=0, column=2, sticky="ns")
        self.image_listbox.configure(yscrollcommand=scrollbar.set)
        
        ttk.Button(list_frame, text="Обновить список", 
                  command=self.refresh_image_list).grid(row=1, column=0, pady=5)
        
        ttk.Button(list_frame, text="Скачать", 
                  command=self.download_image).grid(row=1, column=1, pady=5)
        
        
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1) 
        self.root.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)


    def on_client_select(self, event):
        selection = self.clients_tree.selection()
        if selection:
            item = self.clients_tree.item(selection[0])
            client_id = item['values'][0]
            self.recipient_entry.delete(0, tk.END)
            self.recipient_entry.insert(0, client_id)
        

    def connect_to_server(self):
        self.client.host = self.host_entry.get()
        try:
            self.client.port = int(self.port_entry.get())
        except:
            messagebox.showerror("Ошибка", "Неверный порт")
            return
        
        if self.client.connect():
            self.connect_btn.config(state="disabled")
            self.root.after(2000, self.check_connection)
        else:
            messagebox.showerror("Ошибка", "Не удалось подключиться к серверу")
    

    def check_connection(self):
        if self.client.client_id:
            self.refresh_clients()
            self.refresh_image_list()
        else:
            messagebox.showerror("Ошибка", "Не удалось получить ID от сервера")


    def refresh_clients(self):
        if self.client.client_id:
            self.client.get_connected_clients()


    def update_clients_list(self, clients_dict):
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)
        
        for client_id, client_addr in clients_dict.items():
            if client_id != self.client.client_id:
                self.clients_tree.insert("", "end", values=(client_id, client_addr))
        

    def select_recipient_from_list(self):
        selection = self.clients_tree.selection()
        if selection:
            item = self.clients_tree.item(selection[0])
            client_id = item['values'][0]
            self.recipient_entry.delete(0, tk.END)
            self.recipient_entry.insert(0, client_id)
        else:
            messagebox.showwarning("Предупреждение", "Выберите клиента из списка")
            

    def select_file(self):
        filename = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if filename:
            self.selected_file = filename
            self.file_label.config(text=os.path.basename(filename))
            

    def send_image(self):
        if not hasattr(self, 'selected_file'):
            messagebox.showwarning("Предупреждение", "Сначала выберите файл")
            return
            
        recipient_id = self.recipient_entry.get().strip()
        if not recipient_id:
            messagebox.showwarning("Предупреждение", "Введите ID получателя")
            return
            
        if not self.client.client_id:
            messagebox.showwarning("Предупреждение", "Клиент не подключен к серверу")
            return
            
        def send_thread():
            response = self.client.send_image(self.selected_file, recipient_id)
            # Результат показывается через messagebox в process_server_message
            
        threading.Thread(target=send_thread, daemon=True).start()

        
    def refresh_image_list(self):
        if self.client.client_id:
            self.client.get_image_list()

        
    def update_image_list(self, images):
        self.image_listbox.delete(0, tk.END)
        for image in images:
            self.image_listbox.insert(tk.END, image)
            

    def download_image(self):
        selection = self.image_listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите изображение из списка")
            return
            
        filename = self.image_listbox.get(selection[0])
        
        def download_thread():
            self.client.download_image(filename)
            # Результат показывается через messagebox в receive_image_file
            
        threading.Thread(target=download_thread, daemon=True).start()
            

    def run(self):
        try:
            self.root.mainloop()
        finally:
            self.client.disconnect()


if __name__ == "__main__":
    app = ClientGUI()
    app.run()