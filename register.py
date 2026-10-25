import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget

import test_data

class RegisterWindow(QWidget):

    def __init__(self, login_window):
        super().__init__()
        uic.loadUi("register.ui", self)
        self.login_window = login_window
        self.registerBtn.clicked.connect(self.register)
        self.backBtn.clicked.connect(self.back)

    def back(self):
        self.login_window.show()
        self.close()

    def register(self):
        try:
            login = self.loginEdit.text().strip()
            name = self.nameEdit.text().strip()
            phone = self.phoneEdit.text().strip()
            password = self.passwordEdit.text()
            password2 = self.password2Edit.text()

            if not login or not name or not password or not password2:
                raise ValueError('Заполнены не все поля')

            if not self.phoneEdit.hasAcceptableInput():
                raise ValueError('Введите телефон полностью')

            for user in test_data.USERS:
                if user['login'] == login:
                   raise ValueError('Логин занят')

            if len(password) < 6:
                raise ValueError('Слишком короткий пароль')

            if password != password2:
                raise ValueError('Пароли не совпадают')

            if self.shelterRadio.isChecked():
                role = 'shelter'
            else:
                role = 'user'

            test_data.USERS.append({
                'id': test_data.next_id(test_data.USERS),
                'login': login,
                'password': password,
                'role': role,
                'name': name,
                'phone': phone,
            })

            self.errorLabel.setStyleSheet('color: green;')
            self.errorLabel.setText('Готово! Теперь войдите')

        except ValueError as error:
            self.errorLabel.setStyleSheet("QLabel {color: red;}")
            self.errorLabel.setText('Ошибка: ' + str(error))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegisterWindow(None)
    ex.show()
    sys.exit(app.exec())