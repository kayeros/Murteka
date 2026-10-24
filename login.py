import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget
from register import RegisterWindow

import test_data


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.registerBtn.clicked.connect(self.open_register)
        self.loginBtn.clicked.connect(self.login)
        self.forgotBtn.clicked.connect(self.forgot_password)
        self.passwordEdit.returnPressed.connect(self.login)

    def login(self):
        try:
            login = self.loginEdit.text().strip()
            password = self.passwordEdit.text()
            if not login or not password:
                raise ValueError('введите логин и пароль')

            found = None
            for user in test_data.USERS:
                if user['login'] == login:
                    found = user
            if found is None or found['password'] != password:
                raise ValueError('неверный логин или пароль')

            self.errorLabel.setStyleSheet('color: green;')
            self.errorLabel.setText('Вы вошли: ' + found['name'])
        except ValueError as error:
            self.errorLabel.setStyleSheet('color: red;')
            self.errorLabel.setText('Ошибка: ' + str(error))

    def forgot_password(self):
        self.errorLabel.setStyleSheet('color: red;')
        self.errorLabel.setText('Обратитесь к администратору приюта')

    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginWindow()
    ex.show()
    sys.exit(app.exec())