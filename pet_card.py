import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget
import test_data


class PetCardWindow(QWidget):
    def __init__(self, user, pet_id):
        super().__init__()
        uic.loadUi('pet_card.ui', self)
        self.user = user
        self.pet_id = pet_id

        self.saveBtn.clicked.connect(self.save)

        if self.pet_id is not None:
            self.load_pet()
        else:
            self.statusLabel.setText('Статус: свободен')

        # права доступа: если вошел не приют, запрещаем редактирование
        if self.user['role'] != 'shelter':
            self.nameEdit.setReadOnly(True)
            self.breedEdit.setReadOnly(True)
            self.ageEdit.setReadOnly(True)
            self.descriptionEdit.setReadOnly(True)
            self.catRadio.setEnabled(False)
            self.dogRadio.setEnabled(False)
            self.maleRadio.setEnabled(False)
            self.femaleRadio.setEnabled(False)
            self.saveBtn.setVisible(False)

    def load_pet(self):
        """заполняет поля данными питомца из базы"""
        pet = test_data.find_by_id(test_data.PETS, self.pet_id)
        if pet:
            self.nameEdit.setText(pet['name'])
            self.breedEdit.setText(pet['breed'])
            self.ageEdit.setText(str(pet['age']))
            self.descriptionEdit.setPlainText(pet['description'])

            if pet['kind'] == 'Собака':
                self.dogRadio.setChecked(True)
            else:
                self.catRadio.setChecked(True)

            if pet['sex'] == 'ж':
                self.femaleRadio.setChecked(True)
            else:
                self.maleRadio.setChecked(True)

            self.statusLabel.setText(f"Статус: {pet['status']}")

    def save(self):
        """сохраняет изменения или создает нового питомца"""
        try:
            name = self.nameEdit.text().strip()
            if not name:
                raise ValueError('Кличка не может быть пустой')

            age_text = self.ageEdit.text().strip()
            if not age_text.isdigit():
                raise ValueError('возраст должен быть числом')  # Как в ЛР2
            age = int(age_text)

            kind = 'Собака' if self.dogRadio.isChecked() else 'Кошка'
            sex = 'ж' if self.femaleRadio.isChecked() else 'м'
            breed = self.breedEdit.text().strip()
            description = self.descriptionEdit.toPlainText().strip()

            # если это новый питомец (pet_id is None)
            if self.pet_id is None:
                new_id = test_data.next_id(test_data.PETS)
                test_data.PETS.append({
                    'id': new_id,
                    'shelter_id': self.user['id'],  # ID текущего приюта
                    'name': name,
                    'kind': kind,
                    'breed': breed,
                    'age': age,
                    'sex': sex,
                    'description': description,
                    'status': 'свободен'
                })
                self.pet_id = new_id  # Запоминаем ID, чтобы не создать дубль
                self.statusLabel.setText('Статус: свободен')

            # если это редактирование существующего
            else:
                pet = test_data.find_by_id(test_data.PETS, self.pet_id)
                pet['name'] = name
                pet['kind'] = kind
                pet['breed'] = breed
                pet['age'] = age
                pet['sex'] = sex
                pet['description'] = description

            self.errorLabel.setText("Сохранено ✓")

        except ValueError as error:
            # Ловим ошибку и показываем в errorLabel
            self.errorLabel.setText(str(error))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PetCardWindow(test_data.USERS[0], 1)
    ex.show()
    sys.exit(app.exec())