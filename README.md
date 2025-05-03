# Автомобільна Дошка Оголошень API

Цей проект представляє собою API для сервісу оголошень про продаж автомобілів, розроблений на Django REST Framework.

## Огляд проекту

Система дозволяє користувачам:
- Створювати та керувати оголошеннями про продаж автомобілів
- Виконувати пошук та фільтрацію оголошень за різними параметрами
- Додавати оголошення в обране
- Керувати статусом оголошень (активація, деактивація, видалення)

## Структура проекту

Проект складається з трьох основних додатків:
- users - керування користувачами, профілями та обраними оголошеннями
- cars - управління даними про автомобілі та оголошення
- reviews - система оцінок та відгуків

### Моделі даних

#### Автомобілі
- Brand - бренди автомобілів (Toyota, BMW, тощо)
- CarModel - моделі автомобілів (Camry, X5, тощо)
- BodyType - типи кузовів (седан, хетчбек, тощо)
- Color - кольори автомобілів
- CarProduct - конкретний автомобіль з детальною інформацією
- Advertisement - оголошення про продаж автомобіля

#### Користувачі
- CustomUser - розширена модель користувача
- UserProfile - профіль користувача з додатковою інформацією
- Favorites - обрані оголошення користувача
- SearchHistory - історія пошуку користувача
- Notifications - сповіщення для користувачів

## Встановлення та запуск

### Вимоги
- Python 3.8+
- PostgreSQL
- Django 4.2+

### Кроки встановлення

1. Клонуйте репозиторій:
git clone https://github.com/yourusername/autoriq-marketplace-backend.git

cd autoriq-marketplace-backend

2. Створіть віртуальне середовище та активуйте його:
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

3. Встановіть залежності:
pip install -r requirements.txt

4. Налаштуйте базу даних у settings.py:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
```
5. Виконайте міграції:
python manage.py migrate

6. Заповніть базу даних початковими даними:

python manage.py loaddata car_fixtures.json

7. Створіть суперкористувача:
python manage.py createsuperuser

8. Запустіть сервер:
python manage.py runserver

## API Ендпоінти

### Автентифікація

- POST /api/users/register/ - Реєстрація нового користувача
- POST /api/users/login/ - Отримання JWT токену
- POST /api/users/token/refresh/ - Оновлення JWT токену
- POST /api/users/token/verify/ - Перевірка JWT токену

### Користувачі

- GET/PUT /api/users/profile/me/ - Отримання/оновлення власного профілю
- POST /api/users/profile/change_password/ - Зміна паролю
- GET/POST /api/users/favorites/ - Отримання/додавання обраних оголошень

### Автомобілі

- GET /api/cars/brands/ - Отримання списку брендів
- GET /api/cars/models/?brand=1 - Отримання моделей для конкретного бренду
- GET /api/cars/body-types/ - Отримання типів кузовів
- GET /api/cars/colors/ - Отримання списку кольорів
- GET/POST /api/cars/car-products/ - Отримання/створення автомобілів
- GET/POST /api/cars/advertisements/ - Отримання/створення оголошень
- POST /api/cars/advertisements/{id}/toggle_favorite/ - Додавання/видалення з обраного
- POST /api/cars/advertisements/{id}/activate/ - Активація оголошення
- POST /api/cars/advertisements/{id}/deactivate/ - Деактивація оголошення
- POST /api/cars/advertisements/{id}/soft_delete/ - М'яке видалення оголошення

## Фільтрація та пошук

Система підтримує розширені можливості фільтрації оголошень:

GET /api/cars/advertisements/?min_price=10000&max_price=20000&min_year=2018&brand=Toyota

Доступні фільтри:
- min_price, max_price - діапазон цін
- min_year, max_year - діапазон років випуску
- min_mileage, max_mileage - діапазон пробігу
- brand - пошук за брендом
- model - пошук за моделлю
- search - пошук за ключовими словами в заголовку або описі

## Створення оголошення

Для створення оголошення використовуйте POST-запит:
POST /api/cars/advertisements/
```
{
  "title": "Продаю BMW X5 2020",
  "description": "Відмінний стан, повна комплектація",
  "car_product": {
    "model_id": 6,
    "body_type_id": 4,
    "year": 2020,
    "price": 40000,
    "color_id": 1,
    "mileage": 15000
  }
}
```
## Дозволи (Permissions)

- IsOwnerOrReadOnly - дозволяє редагувати тільки власнику об'єкта
- IsOwner - дозволяє доступ тільки власнику об'єкта
- Більшість ендпоінтів доступні тільки авторизованим користувачам

## Структура коду

- urls.py - маршрутизація API ендпоінтів
- views.py - обробники запитів API
- serializers.py - серіалізатори для перетворення моделей в JSON і назад
- models.py - визначення моделей даних
- filters.py - класи для фільтрації об'єктів

## Використання в адмін-панелі

Система має налаштовану адмін-панель Django, яка дозволяє керувати всіма сутностями проекту:

1. Відкрийте адмін-панель: http://localhost:8000/admin/
2. Увійдіть за допомогою облікових даних суперкористувача
3. Використовуйте інтерфейс для керування брендами, моделями, оголошеннями тощо

## Розробка

<!-- ### Запуск тестів
python manage.py test -->

### Створення нових міграцій
python manage.py makemigrations

## Автори

- https://github.com/maxshymanskiy 