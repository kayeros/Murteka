import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import test_data


from pet_card import PetCardWindow
from rental import RentalWindow
from adoption import AdoptionWindow
from review import ReviewWindow
from shelter import ShelterWindow


class CatalogWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        uic.loadUi('catalog.ui', self)
        self.user = user
        #cписки для хранения данных о питомцах (по индексу строки в списке)
        self.pet_ids = []
        self.shelter_ids = []
        self.statuses = []

        # 1. приветствие
        self.helloLabel.setText(f"Вы вошли: {self.user['name']}")

        # 2. настройка видимости кнопок в зависимости от роли
        if self.user['role'] == 'shelter':
            self.rentBtn.setVisible(False)
            self.adoptBtn.setVisible(False)
            self.reviewBtn.setVisible(False)
        else:
            self.addBtn.setVisible(False)
            self.shelterBtn.setVisible(False)

        # 3. подключение сигналов фильтров
        self.searchEdit.textChanged.connect(self.load_pets)
        self.kindGroup.buttonClicked.connect(self.load_pets)
        self.freeCheck.stateChanged.connect(self.load_pets)
        self.refreshBtn.clicked.connect(self.load_pets)

        # 4. подключение кнопок действий
        self.openBtn.clicked.connect(self.open_card)
        self.addBtn.clicked.connect(self.open_new_card)
        self.rentBtn.clicked.connect(self.open_rental)
        self.adoptBtn.clicked.connect(self.open_adoption)
        self.reviewBtn.clicked.connect(self.open_review)
        self.shelterBtn.clicked.connect(self.open_shelter)

        # 5. первичная загрузка списка питомцев
        self.load_pets()

    def load_pets(self):
        self.petsList.clear()
        self.pet_ids = []
        self.shelter_ids = []
        self.statuses = []

        search = self.searchEdit.text().strip().lower()

        for pet in test_data.PETS:
            # фильтр по поиску (по кличке)
            if search not in pet['name'].lower():
                continue
            # фильтр по виду (Кошки / Собаки)
            if self.catRadio.isChecked() and pet['kind'] != 'Кошка':
                continue
            if self.dogRadio.isChecked() and pet['kind'] != 'Собака':
                continue
            # фильтр "Только свободные"
            if self.freeCheck.isChecked() and pet['status'] != 'свободен':
                continue
            # фильтр для приюта (показываем только его питомцев)
            if self.user['role'] == 'shelter' and pet['shelter_id'] != self.user['id']:
                continue

            # находим имя приюта для отображения
            shelter = test_data.find_by_id(test_data.USERS, pet['shelter_id'])
            shelter_name = shelter['name'] if shelter else "Неизвестно"

            # добавляем в список
            self.petsList.addItem(
                f"{pet['name']}, {pet['kind']}, {pet['breed']}, {pet['age']} г. | {shelter_name} | {pet['status']}")

            # сохраняем ID в списки (они совпадают по индексу со строками в QListView)
            self.pet_ids.append(pet['id'])
            self.shelter_ids.append(pet['shelter_id'])
            self.statuses.append(pet['status'])

        # показываем количество найденных в статусбар
        self.statusbar.showMessage(f'Найдено: {self.petsList.count()}')

    def selected_row(self):
        """проверяет, выбран ли питомец"""
        row = self.petsList.currentRow()  # -1, если ничего не выбрано
        if row == -1:
            raise ValueError('выберите питомца в списке')
        return row

    def open_card(self):
        try:
            row = self.selected_row()
            self.card_window = PetCardWindow(self.user, self.pet_ids[row])
            self.card_window.show()
        except ValueError as error:
            self.statusbar.showMessage('Ошибка: ' + str(error))

    def open_new_card(self):
        # передаем None, чтобы окно поняло, что это новый питомец
        self.card_window = PetCardWindow(self.user, None)
        self.card_window.show()

    def open_rental(self):
        try:
            row = self.selected_row()
            if self.statuses[row] != 'свободен':
                raise ValueError('этот питомец сейчас недоступен')
            self.rental_window = RentalWindow(self.user, self.pet_ids[row])
            self.rental_window.show()
        except ValueError as error:
            self.statusbar.showMessage('Ошибка: ' + str(error))

    def open_adoption(self):
        try:
            row = self.selected_row()
            if self.statuses[row] != 'свободен':
                raise ValueError('этот питомец сейчас недоступен')
            self.adoption_window = AdoptionWindow(self.user, self.pet_ids[row])
            self.adoption_window.show()
        except ValueError as error:
            self.statusbar.showMessage('Ошибка: ' + str(error))

    def open_review(self):
        try:
            row = self.selected_row()
            self.review_window = ReviewWindow(self.user, self.shelter_ids[row])
            self.review_window.show()
        except ValueError as error:
            self.statusbar.showMessage('Ошибка: ' + str(error))

    def open_shelter(self):
        self.shelter_window = ShelterWindow(self.user)
        self.shelter_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CatalogWindow(test_data.USERS[2])
    ex.show()
    sys.exit(app.exec())