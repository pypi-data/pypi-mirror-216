import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QDialog
from ChatWindow.ui_first_form import Ui_Dialog
from PySide6.QtCore import Qt
import hashlib

SALT = b'my_seckret_salt'


class StartWindow(QDialog):
    # message_box = QMessageBox()
    register_flag = False
    join_ok = False
    register_ok = False

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.message_box = QMessageBox()

        self.ui.register_button.clicked.connect(self.button_register_clicked)
        self.ui.join_chat_button.clicked.connect(self.button_join_clicked)
        self.ui.pushButton_exit.clicked.connect(self.exit)
        self.ui.checkBox_exist_user.stateChanged.connect(self.state_exist_box)
        self.ui.checkBox_new_user.stateChanged.connect(self.state_new_box)

        self.show()

    def state_exist_box(self):
        if self.ui.checkBox_exist_user.isChecked():
            self.ui.loginLineEdit.setEnabled(True)
            self.ui.passwordLineEdit.setEnabled(True)
            self.ui.join_chat_button.setEnabled(True)
            self.ui.loginLineEdit_2.setEnabled(False)
            self.ui.passwordLineEdit_2.setEnabled(False)
            self.ui.confrimPasswordLineEdit.setEnabled(False)
            self.ui.register_button.setEnabled(False)
            self.ui.checkBox_new_user.setCheckState(Qt.CheckState.Unchecked)

    def state_new_box(self):
        self.ui.loginLineEdit_2.setEnabled(True)
        self.ui.passwordLineEdit_2.setEnabled(True)
        self.ui.confrimPasswordLineEdit.setEnabled(True)
        self.ui.register_button.setEnabled(True)
        self.ui.loginLineEdit.setEnabled(False)
        self.ui.passwordLineEdit.setEnabled(False)
        self.ui.join_chat_button.setEnabled(False)
        self.ui.checkBox_exist_user.setCheckState(Qt.CheckState.Unchecked)

    def button_register_clicked(self):
        self.login = self.ui.loginLineEdit_2.text()
        _password = self.ui.passwordLineEdit_2.text()
        _confrim_password = self.ui.confrimPasswordLineEdit.text()

        if _password != _confrim_password:
            self.message_box.critical(self, "Warning!", "Entered passwords do not match!",
                                      QMessageBox.StandardButton.Ok)

        else:
            self.register_flag = True
            self.password = hashlib.pbkdf2_hmac(
                'sha256', bytes(_password, 'utf-8'), SALT, 10000)
            _password = None
            _confrim_password = None
            self.register_ok = True
            self.close()

    def button_join_clicked(self):
        self.login = self.ui.loginLineEdit.text()
        self.password = hashlib.pbkdf2_hmac(
            'sha256', bytes(self.ui.passwordLineEdit.text(), 'utf-8'), SALT, 10000)
        self.join_ok = True
        self.close()

    @property
    def hashed_password(self):
        return self.password.hex()

    def exit(self):
        exit(0)


if __name__ == "__main__":
    dialog_app = QApplication(sys.argv)
    dialog_window = StartWindow()
    sys.exit(dialog_app.exec())
