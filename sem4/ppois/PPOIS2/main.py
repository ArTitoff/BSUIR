from model import RecordModel
from controller import Controller
from view import UserPaginationApp
import atexit
import os

def main():

    model = RecordModel()
    controller = Controller(model, None)

    db_file = "mybd.db"
    
    if os.path.exists(db_file):
        model.clients.clear() 
        success, message = controller.load_from_db(db_file)
        if not success:
            print(f"Ошибка при загрузке из БД: {message}")
    view = UserPaginationApp(controller)
    controller.set_view(view)
    def save_on_exit():
        try:
            if os.path.exists(db_file):
                os.remove(db_file)
                
            controller.save_to_db(db_file)
            print("Данные успешно сохранены в БД при выходе")
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
    atexit.register(save_on_exit)
    view.run()

if __name__ == "__main__":
    main()