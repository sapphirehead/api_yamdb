# api_yamdb
***Проект YaMDb***

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Картины» или «Ювелирка»).

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке: git clone git@github.com:YaroslavAndreev/api_yamdb.git
cd api_yamdb

Cоздать и активировать виртуальное окружение: python3 -m venv venv source venv/bin/activate

Установить зависимости из файла requirements.txt: pip3 install -r requirements.txt

Выполнить миграции: python3 manage.py migrate

Запустить проект: python3 manage.py runserver

Документация: Примеры обращений к эндпоинтам находятся по адресу:

http://127.0.0.1:8000/redoc/

Разработчики: Абакумов Максим, Андреев Ярослав, Быков Евгений.
