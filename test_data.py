# Тестовые данные: временная замена базы данных.
# Каждая таблица это список словарей. Ключи словарей = будущие столбцы таблиц в базе.
# Данные живут, пока программа запущена. После перезапуска всё возвращается к этим значениям.

USERS = [
    {'id': 1, 'login': 'shelter1', 'password': '123456', 'role': 'shelter',
     'name': 'Приют «Добрые руки»', 'phone': '+7(912)111-11-11'},
    {'id': 2, 'login': 'shelter2', 'password': '123456', 'role': 'shelter',
     'name': 'Приют «Верный друг»', 'phone': '+7(912)222-22-22'},
    {'id': 3, 'login': 'user1', 'password': '123456', 'role': 'user',
     'name': 'Иван Петров', 'phone': '+7(912)333-33-33'},
]

PETS = [
    {'id': 1, 'shelter_id': 1, 'name': 'Барсик', 'kind': 'Кошка', 'breed': 'беспородный',
     'age': 2, 'sex': 'м', 'description': 'Ласковый, любит спать на коленях.', 'status': 'свободен'},
    {'id': 2, 'shelter_id': 2, 'name': 'Рекс', 'kind': 'Собака', 'breed': 'овчарка',
     'age': 4, 'sex': 'м', 'description': 'Добрый, любит долгие прогулки.', 'status': 'свободен'},
    {'id': 3, 'shelter_id': 1, 'name': 'Мурка', 'kind': 'Кошка', 'breed': 'сиамская',
     'age': 1, 'sex': 'ж', 'description': 'Игривая и очень разговорчивая.', 'status': 'на опеке'},
    {'id': 4, 'shelter_id': 2, 'name': 'Бублик', 'kind': 'Собака', 'breed': 'такса',
     'age': 3, 'sex': 'м', 'description': 'Маленький, но смелый.', 'status': 'свободен'},
    {'id': 5, 'shelter_id': 1, 'name': 'Снежок', 'kind': 'Кошка', 'breed': 'британская',
     'age': 5, 'sex': 'м', 'description': 'Спокойный, подойдёт для квартиры.', 'status': 'свободен'},
    {'id': 6, 'shelter_id': 2, 'name': 'Лайма', 'kind': 'Собака', 'breed': 'дворняга',
     'age': 2, 'sex': 'ж', 'description': 'Очень умная, знает команды.', 'status': 'свободен'},
]

# Заявки на опеку. Одна уже лежит, чтобы кабинету приюта было что показать.
RENTALS = [
    {'id': 1, 'pet_id': 5, 'user_id': 3, 'date_from': '2026-11-01', 'date_to': '2026-11-08',
     'status': 'ожидает'},
]

# Заявки на усыновление.
ADOPTIONS = [
    {'id': 1, 'pet_id': 1, 'user_id': 3, 'reason': 'Есть опыт, живу в просторной квартире.',
     'phone': '+7(912)333-33-33', 'status': 'ожидает'},
]

# Отзывы о приютах.
REVIEWS = [
    {'id': 1, 'shelter_id': 1, 'user_id': 3, 'rating': 5, 'text': 'Очень заботливые, помогли с выбором.'},
]


def find_by_id(table, item_id):
    """Ищет в списке словарь с нужным id. Если не нашёл, возвращает None."""
    for row in table:
        if row['id'] == item_id:
            return row
    return None


def next_id(table):
    """Номер для новой записи: самый большой id + 1."""
    biggest = 0
    for row in table:
        if row['id'] > biggest:
            biggest = row['id']
    return biggest + 1
