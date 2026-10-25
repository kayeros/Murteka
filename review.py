"""Отзывы о приюте и средний рейтинг."""
import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget
import test_data


class ReviewWindow(QWidget):
    def __init__(self, user, shelter_id):
        super().__init__()
        uic.loadUi(str(Path(__file__).with_name('review.ui')), self)
        self.user = user
        self.shelter_id = shelter_id
        self.sendBtn.clicked.connect(self.send)
        self.load_reviews()

    def load_reviews(self):
        shelter = test_data.find_by_id(test_data.USERS, self.shelter_id)
        if shelter is None or shelter['role'] != 'shelter':
            self.shelterLabel.setText('Приют не найден')
            self.avgLabel.setText('Рейтинг недоступен')
            self.errorLabel.setStyleSheet('color: red;')
            self.errorLabel.setText('Не удалось найти приют.')
            self.sendBtn.setEnabled(False)
            self.reviewsList.clear()
            return
        self.shelterLabel.setText('Приют: ' + shelter['name'])
        self.reviewsList.clear()
        ratings = []
        # Показываем только отзывы выбранного приюта.
        for review in test_data.REVIEWS:
            if review['shelter_id'] != self.shelter_id:
                continue
            author = test_data.find_by_id(test_data.USERS, review['user_id'])
            name = author['name'] if author is not None else 'Неизвестный пользователь'
            self.reviewsList.addItem(
                name + ' ' + '★' * review['rating'] + ': ' + review['text'])
            ratings.append(review['rating'])
        # Без этой проверки при пустом списке получилось бы деление на ноль.
        if len(ratings) == 0:
            self.avgLabel.setText('Рейтинг: пока нет отзывов')
        else:
            avg = sum(ratings) / len(ratings)
            self.avgLabel.setText(f'Рейтинг: {avg:.1f} из 5')

    def send(self):
        try:
            button = self.ratingGroup.checkedButton()
            if button is None:
                raise ValueError('поставьте оценку')
            rating = int(button.text())
            text = self.textEdit.toPlainText().strip()
            if not text:
                raise ValueError('напишите текст отзыва')
            if self.user['role'] != 'user':
                raise ValueError('отзыв может оставить только пользователь')
            shelter = test_data.find_by_id(test_data.USERS, self.shelter_id)
            if shelter is None or shelter['role'] != 'shelter':
                raise ValueError('приют не найден')
            test_data.REVIEWS.append({
                'id': test_data.next_id(test_data.REVIEWS),
                'shelter_id': self.shelter_id,
                'user_id': self.user['id'],
                'rating': rating,
                'text': text,
            })
            self.errorLabel.setStyleSheet('color: green;')
            self.errorLabel.setText('Спасибо за отзыв!')
            self.textEdit.clear()
            self.load_reviews()
        except ValueError as error:
            self.errorLabel.setStyleSheet('color: red;')
            self.errorLabel.setText('Ошибка: ' + str(error))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Для проверки приюта без отзывов замените 1 на 2.
    ex = ReviewWindow(test_data.USERS[2], 1)
    ex.show()
    sys.exit(app.exec())
