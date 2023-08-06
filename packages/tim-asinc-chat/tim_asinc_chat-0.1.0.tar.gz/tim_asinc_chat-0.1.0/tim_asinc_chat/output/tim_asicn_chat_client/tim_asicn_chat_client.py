import sys
from PySide6.QtWidgets import QApplication
from gui import My_Window, MsgUpdater, OnlineListUpdater
from first_form import StartWindow
from client_gui import Client


if __name__ == "__main__":
    """
    Файл для запуска Клиентского приложения Чат с графической оболочкой
    """
    client = Client()
    app = QApplication(sys.argv)
    start_window = StartWindow()
    app.exec()
    if start_window.join_ok or start_window.register_ok:
        client_name = start_window.login
        hashed_password = start_window.hashed_password
        register_flag = start_window.register_flag
        del start_window
    else:
        exit(0)
    window = My_Window(client, client_name, hashed_password, register_flag)
    msg_updater = MsgUpdater(client)
    online_status = OnlineListUpdater(client)
    window.start_message_update.connect(msg_updater.start)
    window.ready_to_connection.connect(online_status.start)
    msg_updater.new_message.connect(window.get_new_message)
    sys.exit(app.exec())
