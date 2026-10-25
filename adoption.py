"""Окно заявки на усыновление. Запускать можно отдельно от проекта."""
import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget
import test_data


class AdoptionWindow(QWidget):
    def __init__(self, user, pet_id):
        super().__init__()
        # Форма лежит рядом с кодом; путь работает из любой папки запуска.
        uic.loadUi(str(Path(__file__).with_name('adoption.ui')), self)
        self.user = user
        self.pet_id = pet_id
        self.sendBtn.clicked.connect(self.send)
        self.show_pet_name()

    def show_pet_name(self):
        # find_by_id возвращает словарь питомца или None.
        pet = test_data.find_by_id(test_data.PETS, self.pet_id)
        if pet is None:
            self.petLabel.setText('Питомец не найден')
            self.errorLabel.setText('Не удалось найти питомца. Откройте окно заново из каталога.')
            self.sendBtn.setEnabled(False)
            return
        self.petLabel.setText('Питомец: ' + pet['name'])

    def send(self):
        try:
            reason = self.reasonEdit.toPlainText().strip()
            phone = self.phoneEdit.text()
            if not reason:
                raise ValueError('напишите, почему хотите взять питомца')
            if not self.phoneEdit.hasAcceptableInput():
                raise ValueError('введите телефон полностью')
            if self.user['role'] != 'user':
                raise ValueError('заявку может отправить только пользователь')
            pet = test_data.find_by_id(test_data.PETS, self.pet_id)
            if pet is None:
                raise ValueError('питомец не найден')
            if pet['status'] != 'свободен':
                raise ValueError('питомец сейчас недоступен для усыновления')

            # Запрещаем вторую ожидающую заявку от того же пользователя.
            for adoption in test_data.ADOPTIONS:
                if (adoption['pet_id'] == self.pet_id
                        and adoption['user_id'] == self.user['id']
                        and adoption['status'] == 'ожидает'):
                    raise ValueError('вы уже отправили заявку на этого питомца')

            # Меняем общий список в памяти, а не исходный файл test_data.py.
            test_data.ADOPTIONS.append({
                'id': test_data.next_id(test_data.ADOPTIONS),
                'pet_id': self.pet_id,
                'user_id': self.user['id'],
                'reason': reason,
                'phone': phone,
                'status': 'ожидает',
            })
            self.errorLabel.setStyleSheet('color: green;')
            self.errorLabel.setText('Заявка отправлена! Приют свяжется с вами.')
            self.sendBtn.setEnabled(False)
        except ValueError as error:
            self.errorLabel.setStyleSheet('color: red;')
            self.errorLabel.setText('Ошибка: ' + str(error))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Рекс (id 2): на него ещё нет заявки Ивана. Для проверки дубля поставить 1.
    ex = AdoptionWindow(test_data.USERS[2], 2)
    ex.show()
    sys.exit(app.exec())
