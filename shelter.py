import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6 import uic
import test_data


class ShelterWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        uic.loadUi('shelter.ui', self)

        self.user = user

        self.setWindowTitle(f"Муртека: {self.user['name']}")
        self.titleLabel.setText(f"Кабинет: {self.user['name']}")

        # Вкладка 1 (Новые заявки)
        self.tabWidget.widget(0).findChild(type(self.tabWidget.widget(0)), "").findChild  # просто для инициализации
        self.approveBtn.clicked.connect(self.approve)
        self.rejectBtn.clicked.connect(self.reject)
        self.refreshBtn1.clicked.connect(self.load_all)

        self.refreshBtn2.clicked.connect(self.load_all)

        self.editBtn.clicked.connect(self.open_pet_card)
        self.deleteBtn.clicked.connect(self.delete_pet)
        self.load_all()

    def load_all(self):
        """Обновляет все списки и статистику"""
        self.load_requests()
        self.load_history()
        self.load_stats()
        self.load_pets()

    def load_requests(self):
        """Загружает новые заявки (ожидают)"""
        self.requestsList.clear()
        self.requests = []

        # Ищем заявки на ОПЕКУ
        for r in test_data.RENTALS:
            pet = test_data.find_by_id(test_data.PETS, r['pet_id'])
            if pet and pet['shelter_id'] == self.user['id'] and r['status'] == 'ожидает':
                person = test_data.find_by_id(test_data.USERS, r['user_id'])
                text = f"Опека: {pet['name']} | {person['name']} | {r['date_from']} – {r['date_to']}"
                self.requestsList.addItem(text)
                self.requests.append(('rental', r))

        for a in test_data.ADOPTIONS:
            pet = test_data.find_by_id(test_data.PETS, a['pet_id'])
            if pet and pet['shelter_id'] == self.user['id'] and a['status'] == 'ожидает':
                person = test_data.find_by_id(test_data.USERS, a['user_id'])
                text = f"Усыновление: {pet['name']} | {person['name']} | тел. {a['phone']} | «{a['reason']}»"
                self.requestsList.addItem(text)
                self.requests.append(('adoption', a))

        self.countReq1.setText(f"Всего заявок: {self.requestsList.count()}")

    def load_history(self):
        """Загружает рассмотренные заявки"""
        self.historyList.clear()
        count = 0

        for r in test_data.RENTALS:
            pet = test_data.find_by_id(test_data.PETS, r['pet_id'])
            if pet and pet['shelter_id'] == self.user['id'] and r['status'] != 'ожидает':
                person = test_data.find_by_id(test_data.USERS, r['user_id'])
                text = f"Опека: {pet['name']} | {person['name']} | {r['date_from']} – {r['date_to']} | {r['status']}"
                self.historyList.addItem(text)
                count += 1

        for a in test_data.ADOPTIONS:
            pet = test_data.find_by_id(test_data.PETS, a['pet_id'])
            if pet and pet['shelter_id'] == self.user['id'] and a['status'] != 'ожидает':
                person = test_data.find_by_id(test_data.USERS, a['user_id'])
                text = f"Усыновление: {pet['name']} | {person['name']} | {a['status']}"
                self.historyList.addItem(text)
                count += 1

        self.countReq2.setText(f"Всего заявок: {count}")

    def load_stats(self):
        """Считает статистику приюта"""
        sid = self.user['id']
        total = free = rented = adopted = 0

        for pet in test_data.PETS:
            if pet['shelter_id'] == sid:
                total += 1
                if pet['status'] == 'свободен':
                    free += 1
                elif pet['status'] == 'на опеке':
                    rented += 1
                elif pet['status'] == 'усыновлён':
                    adopted += 1

        ratings = []
        for r in test_data.REVIEWS:
            if r['shelter_id'] == sid:
                ratings.append(r['rating'])

        if not ratings:
            rating_text = 'нет отзывов'
        else:
            rating_text = f'{sum(ratings) / len(ratings):.1f}'

        stats_text = f"Всего питомцев: {total}\nСвободны: {free}\nНа опеке: {rented}\nУсыновлены: {adopted}\nРейтинг: {rating_text}"
        self.statsLabel.setText(stats_text)

    def load_pets(self):
        """Загружает питомцев этого приюта"""
        self.listPets.clear()
        self.pet_ids = []
        for pet in test_data.PETS:
            if pet['shelter_id'] == self.user['id']:
                self.listPets.addItem(f"{pet['name']} ({pet['kind']}) — {pet['status']}")
                self.pet_ids.append(pet['id'])

    def approve(self):
        row = self.requestsList.currentRow()
        if row == -1:
            self.errorLabel.setText('Ошибка: выберите заявку в списке!')
            return

        kind, request = self.requests[row]
        pet = test_data.find_by_id(test_data.PETS, request['pet_id'])

        if pet['status'] != 'свободен':
            self.errorLabel.setText(f"Ошибка: {pet['name']} уже занят!")
            return

        request['status'] = 'одобрено'
        if kind == 'rental':
            pet['status'] = 'на опеке'
        else:
            pet['status'] = 'усыновлён'

        self.errorLabel.setText(f'Заявка на {pet["name"]} одобрена!')
        self.load_all()

    def reject(self):
        row = self.requestsList.currentRow()
        if row == -1:
            self.errorLabel.setText('Ошибка: выберите заявку в списке!')
            return

        kind, request = self.requests[row]
        request['status'] = 'отклонено'

        self.errorLabel.setText('Заявка отклонена.')
        self.load_all()

    def open_pet_card(self):
        row = self.listPets.currentRow()
        if row == -1:
            self.errorLabel.setText('Выберите питомца.')
            return

        pet_id = self.pet_ids[row]
        self.errorLabel.setText(f'Открывается карточка питомца (ID: {pet_id})')

    def delete_pet(self):
        row = self.listPets.currentRow()
        if row == -1:
            self.errorLabel.setText('Выберите питомца.')
            return

        pet_id = self.pet_ids[row]
        pet = test_data.find_by_id(test_data.PETS, pet_id)

        reply = QMessageBox.question(self, 'Удаление', f'Удалить {pet["name"]}?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            test_data.PETS.remove(pet)
            self.errorLabel.setText(f'Питомец {pet["name"]} удален.')
            self.load_all()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShelterWindow(test_data.USERS[0])
    ex.show()
    sys.exit(app.exec())