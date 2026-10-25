import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtCore import QDate
from PyQt6 import uic
import test_data


class RentalWindow(QWidget):
    def __init__(self, user, pet_id):
        super().__init__()
        uic.loadUi('rental.ui', self)

        self.user = user
        self.pet_id = pet_id

        self.pet = test_data.find_by_id(test_data.PETS, self.pet_id)
        if self.pet:
            self.petLabel.setText('Питомец: ' + self.pet['name'])

        today = QDate.currentDate()

        self.dateFromEdit.setMinimumDate(today)
        self.dateFromEdit.setDate(today)

        self.dateToEdit.setMinimumDate(today.addDays(1))
        self.dateToEdit.setDate(today.addDays(7))
        self.dateFromEdit.dateChanged.connect(self.update_days)
        self.dateToEdit.dateChanged.connect(self.update_days)
        self.sendBtn.clicked.connect(self.send)
        self.update_days()

    def update_days(self):
        days = self.dateFromEdit.date().daysTo(self.dateToEdit.date())
        self.daysLabel.setText(f'Срок: {days} дн.')

    def send(self):
        try:
            days = self.dateFromEdit.date().daysTo(self.dateToEdit.date())

            if days < 1:
                raise ValueError('Дата окончания должна быть позже даты начала')

            if days > 30:
                raise ValueError('Опека не может быть дольше 30 дней')

            if self.pet['status'] != 'свободен':
                raise ValueError('Питомец уже на передержке!')

            for r in test_data.RENTALS:
                if r['pet_id'] == self.pet_id and r['user_id'] == self.user['id'] and r['status'] == 'ожидает':
                    raise ValueError('Вы уже отправили заявку на этого питомца')

            test_data.RENTALS.append({
                'id': test_data.next_id(test_data.RENTALS),
                'pet_id': self.pet_id,
                'user_id': self.user['id'],
                'date_from': self.dateFromEdit.date().toString('yyyy-MM-dd'),
                'date_to': self.dateToEdit.date().toString('yyyy-MM-dd'),
                'status': 'ожидает',
            })

            self.errorLabel.setStyleSheet("color: green; font-weight: bold;")
            self.errorLabel.setText('Заявка отправлена! Ждите решения приюта')
            self.sendBtn.setEnabled(False)

        except ValueError as error:
            self.errorLabel.setStyleSheet("color: red; font-weight: bold;")
            self.errorLabel.setText(str(error))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RentalWindow(test_data.USERS[2], 2)
    ex.show()
    sys.exit(app.exec())