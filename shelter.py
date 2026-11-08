import sys
import os
import shutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QFileDialog, QHeaderView
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
import test_data


class ShelterWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        uic.loadUi('shelter.ui', self)

        self.user = user

        self.setWindowTitle("Муртека: Кабинет приюта")
        self.approveBtn.clicked.connect(self.approve)
        self.rejectBtn.clicked.connect(self.reject)
        self.refreshBtn1.clicked.connect(self.load_all)
        self.refreshBtn2.clicked.connect(self.load_all)
        self.editBtn.clicked.connect(self.open_pet_card)
        self.deleteBtn.clicked.connect(self.delete_pet)

        if hasattr(self, 'editProfileBtn'):
            self.editProfileBtn.clicked.connect(self.change_logo)

        self.load_all()
        self.load_shelter_profile()

    def load_all(self):
        self.load_requests()
        self.load_history()
        self.load_stats()
        self.load_pets()

    def load_shelter_profile(self):
        """Загружает имя, телефон и логотип приюта в визитку"""
        self.shelterNameLabel.setText(self.user['name'])
        self.shelterPhoneLabel.setText(f"Тел: {self.user['phone']}")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_file = os.path.join(current_dir, 'logo.jpg')

        if os.path.exists(logo_file) and hasattr(self, 'pic'):
            pixmap = QPixmap(logo_file)
            # Ставим картинку и масштабируем под размер лейбла
            self.pic.setPixmap(pixmap.scaled(
                200, 200,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        elif hasattr(self, 'pic'):
            self.pic.setText("Логотип не найден")
            print(f"Искал файл тут: {logo_file}")  # Выведет путь в консоль для проверки

    def change_logo(self):
        """Открывает окно выбора файла для загрузки нового логотипа"""
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите логотип", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            new_logo_name = f"shelter_{self.user['id']}.png"
            shutil.copy(file_name, new_logo_name)
            self.load_shelter_profile()
            self.errorLabel.setText("Логотип обновлен!")

    def load_requests(self):
        """Загружает новые заявки в таблицу requestsTable"""
        self.requestsTable.setRowCount(0)
        self.requests = []
        row = 0

        # Заявки на ОПЕКУ
        for r in test_data.RENTALS:
            pet = test_data.find_by_id(test_data.PETS, r['pet_id'])
            if pet and pet['shelter_id'] == self.user['id'] and r['status'] == 'ожидает':
                person = test_data.find_by_id(test_data.USERS, r['user_id'])
                self.requestsTable.insertRow(row)
                self.requestsTable.setItem(row, 0, QTableWidgetItem("Опека"))
                self.requestsTable.setItem(row, 1, QTableWidgetItem(pet['name']))
                self.requestsTable.setItem(row, 2, QTableWidgetItem(person['name']))
                self.requestsTable.setItem(row, 3, QTableWidgetItem(f"{r['date_from']} - {r['date_to']}"))
                self.requestsTable.setItem(row, 4, QTableWidgetItem(r['status']))
                self.requests.append(('rental', r))
                row += 1

        # Заявки на УСЫНОВЛЕНИЕ
        for a in test_data.ADOPTIONS:
            pet = test_data.find_by_id(test_data.PETS, a['pet_id'])
            if pet and pet['shelter_id'] == self.user['id'] and a['status'] == 'ожидает':
                person = test_data.find_by_id(test_data.USERS, a['user_id'])
                self.requestsTable.insertRow(row)
                self.requestsTable.setItem(row, 0, QTableWidgetItem("Усыновление"))
                self.requestsTable.setItem(row, 1, QTableWidgetItem(pet['name']))
                self.requestsTable.setItem(row, 2, QTableWidgetItem(person['name']))
                self.requestsTable.setItem(row, 3, QTableWidgetItem(f"Тел: {a['phone']}"))
                self.requestsTable.setItem(row, 4, QTableWidgetItem(a['status']))
                self.requests.append(('adoption', a))
                row += 1

        # Настройка ширины колонок: Инфо (3) растягивается, остальные по размеру текста
        header = self.requestsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) # Инфо растягивается
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.requestsTable.setColumnWidth(4, 120) # Фиксируем ширину "Действие"

        self.countReq1.setText(f"Всего заявок: {self.requestsTable.rowCount()}")

    def load_history(self):
        """Загружает рассмотренные заявки в таблицу historyTable"""
        self.historyTable.setRowCount(0)
        row = 0

        for r in test_data.RENTALS:
            pet = test_data.find_by_id(test_data.PETS, r['pet_id'])
            if pet and pet['shelter_id'] == self.user['id'] and r['status'] != 'ожидает':
                person = test_data.find_by_id(test_data.USERS, r['user_id'])
                self.historyTable.insertRow(row)
                self.historyTable.setItem(row, 0, QTableWidgetItem("Опека"))
                self.historyTable.setItem(row, 1, QTableWidgetItem(pet['name']))
                self.historyTable.setItem(row, 2, QTableWidgetItem(person['name']))
                self.historyTable.setItem(row, 3, QTableWidgetItem(f"{r['date_from']} - {r['date_to']}"))
                self.historyTable.setItem(row, 4, QTableWidgetItem(r['status']))
                row += 1

        for a in test_data.ADOPTIONS:
            pet = test_data.find_by_id(test_data.PETS, a['pet_id'])
            if pet and pet['shelter_id'] == self.user['id'] and a['status'] != 'ожидает':
                person = test_data.find_by_id(test_data.USERS, a['user_id'])
                self.historyTable.insertRow(row)
                self.historyTable.setItem(row, 0, QTableWidgetItem("Усыновление"))
                self.historyTable.setItem(row, 1, QTableWidgetItem(pet['name']))
                self.historyTable.setItem(row, 2, QTableWidgetItem(person['name']))
                self.historyTable.setItem(row, 3, QTableWidgetItem(f"Тел: {a['phone']}"))
                self.historyTable.setItem(row, 4, QTableWidgetItem(a['status']))
                row += 1

        header = self.historyTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) # Инфо растягивается
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)

        self.countReq2.setText(f"Всего заявок: {self.historyTable.rowCount()}")

    def load_stats(self):
        """Считает статистику"""
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

        ratings = [r['rating'] for r in test_data.REVIEWS if r['shelter_id'] == sid]
        rating_text = f'{sum(ratings) / len(ratings):.1f}' if ratings else 'нет отзывов'

        stats_text = f"Всего питомцев: {total}\nСвободны: {free} | На опеке: {rented} | Усыновлены: {adopted}\nРейтинг: {rating_text} ★"
        self.statsLabel.setText(stats_text)

    def load_pets(self):
        """Загружает питомцев в таблицу petsTable"""
        self.petsTable.setRowCount(0)
        self.pet_ids = []
        row = 0

        for pet in test_data.PETS:
            if pet['shelter_id'] == self.user['id']:
                self.petsTable.insertRow(row)

                self.petsTable.setItem(row, 0, QTableWidgetItem(pet['name']))     # Кличка
                self.petsTable.setItem(row, 1, QTableWidgetItem(pet['kind']))     # Вид
                self.petsTable.setItem(row, 2, QTableWidgetItem(str(pet['age'])))# Возраст
                self.petsTable.setItem(row, 3, QTableWidgetItem(pet['status']))  # Статус

                self.pet_ids.append(pet['id'])
                row += 1

        header = self.petsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) # Инфо растягивается
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.petsTable.setColumnWidth(4, 120) # Фиксируем ширину "Действие"

    def approve(self):
        row = self.requestsTable.currentRow()
        if row == -1:
            self.errorLabel.setText('Ошибка: выберите заявку!')
            return
        kind, request = self.requests[row]
        pet = test_data.find_by_id(test_data.PETS, request['pet_id'])
        if pet['status'] != 'свободен':
            self.errorLabel.setText(f"Ошибка: {pet['name']} уже занят!")
            return
        request['status'] = 'одобрено'
        pet['status'] = 'на опеке' if kind == 'rental' else 'усыновлён'
        self.errorLabel.setText(f'Заявка на {pet["name"]} одобрена!')
        self.load_all()

    def reject(self):
        row = self.requestsTable.currentRow()
        if row == -1:
            self.errorLabel.setText('Ошибка: выберите заявку!')
            return
        kind, request = self.requests[row]
        request['status'] = 'отклонено'
        self.errorLabel.setText('Заявка отклонена.')
        self.load_all()

    def open_pet_card(self):
        row = self.petsTable.currentRow()
        if row == -1:
            self.errorLabel.setText('Выберите питомца.')
            return
        pet_id = self.pet_ids[row]
        self.errorLabel.setText(f'Открывается карточка (ID: {pet_id})')

    def delete_pet(self):
        row = self.petsTable.currentRow()
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