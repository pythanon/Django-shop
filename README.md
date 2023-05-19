# Магазин  Django

### Установка:
**1. Установить и активировать виртуальную среду.**
```
pip install virtualenv
python -m venv venv
venv/scripts/activate
```
**2. Кнонировать репозиторий.**
```
git clone https://gitlab.skillbox.ru/aleksandr_chernykh_1/Python_django_diploma_dpo.git
```
**3. Установка зависимостей.**
```
pip install -r requirements.txt
```
**4. Создать ".env" файл по шаблону ".env.template". Прописать адрес и пароль почты для отправки писем с восстановлением пароля.**

**5. Создать и применить миграции.** 
```
python manage.py makemigrations
python manage.py migrate
```
**6. Импортировать фикстуры.**
```
python manage.py loaddata fixtures.json
Логин/пароль:
Админ: admin:linux
Тестовый юзер: test1:123test123
```
**7. Запуск сервера.**
```
python manage.py runserver
```
