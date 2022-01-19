# praktikum_new_diplom
# Дипломный проект курса Python-разработчик Яндекс-Практикум
 
***
### описание:
С помощью сервиса Foodgram - продуктовый помощник, пользователи смогут публиковать рецепты, подписываться на других пользователей, фильтровать рецепты по тегам, добавлять понравившиеся рецепты в список "Избранное" и скачивать список продуктов из "Избранное" в файл.
*** 
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/iogin/foodgram-project-react.git
```

Установить docker и docker-compose:

```
Инструкция по установке доступна в официальной инструкции
```
Создать файл .env с переменными окружения:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres # Имя базы данных
POSTGRES_USER=postgres # Администратор базы данных
POSTGRES_PASSWORD=postgres # Пароль администратора
DB_HOST=db
DB_PORT=5432
```
Сборка и запуск контейнера:

```
docker-compose up -d --build
```

Сбор статики:

```
docker-compose exec web python manage.py collectstatic --noinput
```

Создание суперпользователя Django:

```
docker-compose exec web python manage.py createsuperuser
```



Сервис доступен по адресу:
http://www.eklmn.space

Автор проекта: Кириленко Инесса 

