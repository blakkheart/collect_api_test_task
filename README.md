
# 💸 Сбор денег API 💸

## Описание

Проект выполнен в качестве тестового задания для команды Пронин-team.

API сервис позволяет создать Групповой сбор денег. Сбор можно создавать без верхней границы. Создание доступно только авторизованным пользователям, редактирование и удаление только создателю Группового сбора.
Платеж можно отправлять, будучи неавторизованным.
Платеж можно отправлять, скрывая данные о количестве денег. Есть возможность посмотреть все свои платежи.
Если платеж отправлен от лица авторизованного пользователя, то данные о почте, имени и фамилии автоматически изменятся на те, что указаны в профиле.
При создании Группового сбора или Платежа на почту создателя сбора/платежа приходит письмо с информацией об успешном создании сбора (отправке платежа).

## Стэк технологий

- [Django ](https://www.djangoproject.com/) — фреймворк.
- [Django REST framework](https://www.django-rest-framework.org/) — реализация REST API.
- [PostgreSQL](https://www.postgresql.org/) — база данных приложения.
- [Redis](https://redis.io/)  — для кэширования GET запросов к эндпоинтам.
- [Celery](https://docs.celeryq.dev/en/stable/) — для реализации отправки Email в качестве фоновых задач.
- [Factory Boy](https://factoryboy.readthedocs.io/en/stable/) — для наполнения БД моковыми данными.
- [Docker](https://www.docker.com/) — контейнеризация приложения.
- [Nginx](https://www.nginx.com/)  — для раздачи статики в docker.

## Установка

1. Склонируйте репозиторий:
```bash
git clone https://github.com/blakkheart/collect_api_test_task.git
```
2. Перейдите в директорию проекта:
```bash
cd collect_api_test_task
```
3. Установите и активируйте виртуальное окружение:
   - Windows
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```
   - Linux/macOS
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Обновите [pip](https://pip.pypa.io/en/stable/):
   - Windows
   ```bash
   (venv) python -m pip install --upgrade pip
   ```
   - Linux/macOS
   ```bash
   (venv) python3 -m pip install --upgrade pip
   ```
5. Установите зависимости из файла requirements.txt:
   ```bash
   (venv) pip install -r backend/requirements.txt
   ```
Создайте и заполните файл `.env` по примеру с файлом `.env.example`, который находится в корневой директории.



## Использование  

1. Введите команду для запуска докер-контейнера:
	```bash
	docker compose up
	```
2. Создайте и примените миграции: 
	```bash
	docker compose exec backend python manage.py makemigrations
	docker compose exec backend python manage.py migrate
	```
4. Соберите и скопируйте статику:
	```bash
	docker compose exec backend python manage.py collectstatic
	docker compose exec backend cp -r /app/static/. /backend_static/static
	```
Cервер запустится по адресу **localhost:8000** и вы сможете получить доступ к API.

Доступны эндпоинты:
 - **localhost:8000/api/v1/auth/users**   —   POST запрос для регистрации пользователя c параметрами:
	 ```json
	 {
	 "email": "string",
	 "username": "string"
	 "password": "string",
	 "first_name": "string",
	 "last_name": "string"
	 }
	 ```
  - **localhost:8000/api/v1/auth/token/login/**   —   POST запрос для получения токена c параметрами:
	  ```json
	  {
	 "email": "string",
	 "password": "string"
	 }
	  ```
- **localhost:8000/api/v1/collections/**   —   GET, POST запросы для получения всех Групповых сборов / создания сбора с параметрами:
	 ```json
	{
	"title": "string",
	"reasons": {
	    "title": "string"
	  },
	"description": "string",
	"amount_to_collect": 2147483647,
	"cover_image": "string",
	"end_datetime": "2024-02-29T14:02:38.659Z"
	}
	```
 - **localhost:8000/api/v1/collections/{id}/**   — GET, PATCH, DELETE запросы для получения/ изменения (только автор) и удаления (только автор) конкретного сбора.
 -  **localhost:8000/api/v1/collections/{collection_id}/payments/**   — GET и POST запросы для получения платежей для сбора и создания платежа с параметрами:
	  ```json
      "amount": 2147483647,
      "invisible": true,
      "first_name_user": "string",
      "last_name_user": "string",
      "email_user": "user@example.com"
	  ```
-  **localhost:8000/api/v1/collections/{collection_id}/payments/{id}**   — GET запрос для получения конкретного платежа.
 -  **localhost:8000/api/v1/reasons/**   — GET и POST запросы для получения причин для сбора и создания причины с параметрами:
	  ```json
      "title": "string"
	  ```
 -  **localhost:8000/api/v1/reasons/{id}**   — GET запрос для получения причины для сбора.

- **localhost:8000/api/v1/user/payments/**   — GET запрос для получения всех платежей зарегистрированного пользователя.
 - **localhost:8000/api/v1/docs/** - документация проекта.
- **localhost:8000/admin/** - админ панель проекта.

### Дополнительно
Вы можете создать суперпользователя и изменять значения через админ-панель по адресу **localhost:8000/admin/** :
``bash
docker compose exec backend python manage.py createsuperuser
``
Вы также можете наполнить БД проекта мок-датой с помощью следующей команды:
``bash
docker compose exec backend python manage.py load_mockdata
``
С использованием параметра `-a (--amount)` вы можете задать количество мок-объектов, которые будут занесены в БД (стандартное значение 10).
Например, с помощью команды ниже можно занести 100 мок-объектов в БД:	
``bash
docker compose exec backend python manage.py load_mockdata --amount 100
``