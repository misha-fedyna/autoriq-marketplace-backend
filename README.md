# 🚀 Документація backend-частини маркетплейсу AutoRIQ

Цей документ надає детальні інструкції з налаштування та використання backend-частини маркетплейсу AutoRIQ, API на базі Django REST для платформи автомобільних оголошень.

## 📋 Огляд проєкту

AutoRIQ — це онлайн-маркетплейс для автомобільних оголошень з наступними функціями:
- 🔐 Автентифікація користувачів та управління профілем
- 🚗 Створення та управління автомобільними оголошеннями
- ⭐ Система обраних оголошень
- 🔍 Розширений пошук та фільтрація оголошень

## 🛠️ Технічний стек

- 🐍 Python 3.12+
- 🧩 Django 5.1
- 🌐 Django REST Framework
- 🐘 PostgreSQL
- 🔑 JWT Автентифікація

## 📥 Встановлення

### Передумови

- 🐍 Python 3.12 або вище
- 🐘 PostgreSQL
- 📂 Git

### Кроки налаштування

1. **Клонування репозиторію** 📋
   ```bash
   git clone https://github.com/your-username/autoriq-marketplace-backend.git
   cd autoriq-marketplace-backend
   ```

2. **Створення віртуального середовища** 🔮
   ```bash
   # Створюємо віртуальне середовище
   python -m venv venv
   
   # На Windows
   venv\Scripts\activate
   
   # На macOS/Linux
   source venv/bin/activate
   ```

3. **Встановлення залежностей** 📦
   ```bash
   # Встановлюємо всі необхідні пакети
   pip install -r requirements.txt
   ```

4. **Створення файлу середовища** ⚙️
   
   Створіть файл .env.local в кореневому каталозі проєкту з:
   ```env
   # Важливі налаштування для роботи застосунку
   DJANGO_SECRET_KEY='your-secret-key'
   DEBUG=True
   DATABASE_URL=postgres://postgres:postgres@localhost:5432/testServer1
   ```

## 🗄️ Налаштування бази даних

1. **Встановіть PostgreSQL**, якщо він ще не встановлений

2. **Створення бази даних** 🐘
   ```bash
   # Створення бази даних для проєкту
   createdb testServer1
   ```
   Або використовуйте pgAdmin чи інший інструмент управління PostgreSQL

3. **Налаштування параметрів бази даних** ⚙️
   
   Стандартна конфігурація в settings.py:
   ```python
   # Конфігурація підключення до бази даних
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'testServer1',
           'USER': 'postgres',
           'PASSWORD': 'postgres',
           'HOST': 'localhost',
           'PORT': '5432'
       }
   }
   ```
   
   За потреби змініть ці налаштування у своєму файлі .env.local.

## ▶️ Запуск додатку

1. **Застосування міграцій** 🔄
   ```bash
   cd project
   
   # Застосовуємо міграції до бази даних
   python manage.py migrate
   ```

2. **Створення суперкористувача** 👑
   ```bash
   # Створюємо адміністратора системи
   python manage.py createsuperuser
   ```
   Слідуйте підказкам для створення облікового запису адміністратора

3. **Запуск сервера розробки** 🚀
   ```bash
   # Запускаємо сервер на порту 8008
   python manage.py runserver
   ```
   
   API буде доступне за адресою http://127.0.0.1:8008/

## ✅ Запуск тестів

Проєкт використовує pytest для тестування:

```bash
# Запуск усіх тестів
pytest

# Запуск з детальним виводом
pytest -v
```

Для певних тестових файлів:

```bash
# Тестування тільки автентифікації
pytest project/users/tests/api/test_auth.py
```

## 📡 Документація API

### 🔐 Ендпоінти автентифікації

**JWT Автентифікація**
- `POST /api/users/auth/jwt/create/` - Отримати JWT токен
- `POST /api/users/auth/jwt/refresh/` - Оновити JWT токен
- `POST /api/users/auth/jwt/verify/` - Перевірити JWT токен

**Приклад:** 💻
```bash
# Логін та отримання токенів
curl -X POST http://localhost:8008/api/users/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "yourpassword"}'
```

### 👤 Ендпоінти користувачів

- `GET /api/users/profile/me/` - Отримати поточний профіль користувача
- `PUT /api/users/profile/update_me/` - Оновити профіль користувача
- `GET /api/users/favorites/` - Список обраних оголошень користувача
- `POST /api/users/favorites/` - Додати оголошення до обраних

**Приклад:** 💻
```bash
# Отримати профіль користувача з JWT токеном
curl -X GET http://localhost:8008/api/users/profile/me/ \
  -H "Authorization: Bearer <your_jwt_token>"
```

### 🚗 Ендпоінти оголошень про автомобілі

- `GET /api/cars/advertisements/` - Список всіх оголошень
- `POST /api/cars/advertisements/` - Створити нове оголошення
- `GET /api/cars/advertisements/{id}/` - Отримати деталі оголошення
- `PUT /api/cars/advertisements/{id}/` - Оновити оголошення
- `DELETE /api/cars/advertisements/{id}/` - Видалити оголошення
- `POST /api/cars/advertisements/{id}/toggle_favorite/` - Додати/видалити з обраних
- `POST /api/cars/advertisements/{id}/activate/` - Активувати оголошення
- `POST /api/cars/advertisements/{id}/deactivate/` - Деактивувати оголошення
- `POST /api/cars/advertisements/{id}/soft_delete/` - М'яке видалення оголошення

**Приклад - Створення оголошення:** 💻
```bash
# Створення нового оголошення з фото
curl -X POST http://localhost:8008/api/cars/advertisements/ \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: multipart/form-data" \
  -F "title=BMW X5 2022" \
  -F "description=Відмінний стан" \
  -F "price=50000" \
  -F "brand=BMW" \
  -F "model_name=X5" \
  -F "year=2022" \
  -F "body_type=suv" \
  -F "drive_type=awd" \
  -F "power=300" \
  -F "transmission=automatic" \
  -F "color=black" \
  -F "mileage=5000" \
  -F "door_count=5" \
  -F "fuel_type=diesel" \
  -F "engine_capacity=3.0" \
  -F "city=Київ" \
  -F "main_photo=@/path/to/photo.jpg"
```

### 🔍 Розширена фільтрація

API підтримує розширену фільтрацію оголошень:

```bash
# Пошук дизельних Toyota вартістю від 10000 до 30000
GET /api/cars/advertisements/?min_price=10000&max_price=30000&brand=Toyota&fuel_type=diesel
```

Доступні фільтри:
- 💰 `min_price`, `max_price` - діапазон ціни
- 📅 `min_year`, `max_year` - діапазон року випуску
- 🛣️ `min_mileage`, `max_mileage` - діапазон пробігу
- ⚡ `min_power`, `max_power` - діапазон потужності двигуна
- 🔧 `min_engine_capacity`, `max_engine_capacity` - діапазон об'єму двигуна
- 🏭 `brand` - марка автомобіля
- 🚙 `model` - модель автомобіля
- 🏙️ `city` - місто
- 🚗 `body_type`, `drive_type`, `transmission`, `color`, `fuel_type` - характеристики автомобіля
- 🔍 `search` - повнотекстовий пошук за заголовком, описом, брендом, моделлю тощо

## 📁 Структура проєкту

- project - корінь Django проєкту
  - 👤 `users/` - додаток управління користувачами
  - 🚗 `cars/` - додаток автомобільних оголошень
  - 🔌 `api/` - маршрутизація API
  - ⚙️ project - налаштування проєкту

## 👨‍💼 Інтерфейс адміністратора

Адмін-інтерфейс Django доступний за адресою http://localhost:8008/admin/ після входу з обліковими даними суперкористувача.

Адміністративний інтерфейс забезпечує повні можливості CRUD для:
- 👥 Управління користувачами
- 🚗 Управління оголошеннями
- 👤 Профілі користувачів та обрані оголошення

## 💻 Розробка

Щоб створити нові міграції бази даних:

```bash
# Створення міграцій після змін моделей
python manage.py makemigrations

# Показати SQL для міграцій (корисно для перевірки)
python manage.py sqlmigrate app_name 0001
```

## 📝 Ліцензія

Цей проєкт є власністю замовника і не ліцензований для публічного використання.

---
### 💡 Порада
Для зручного тестування API рекомендуємо використовувати Postman або інтерактивну документацію, доступну за адресою http://localhost:8008/api/schema/swagger-ui/