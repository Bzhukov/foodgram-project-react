# praktikum_new_diplom

### Описание

сайт Foodgram это онлайн-сервис «Продуктовый помощник». На этом сервисе
пользователи смогут публиковать рецепты, подписываться на публикации других
пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед
походом в магазин скачивать сводный список продуктов, необходимых для
приготовления одного или нескольких выбранных блюд.

### Установка:

1) Запустите терминал и откройте в нем папку, в которую хотите клонировать
   проект.
2) Клонируйте репозиторий:

```
git clone git@github.com:Bzhukov/foodgram-project-react.git
```

3) Перейдите в папку infra и переименуйте файл example.env в .env и заполните
   данными для подключения к бд:

```
cd infra/
mv example.env .env
nano example.env
```

В файле необходимо указать данные для подключения к базе данных.

**Формат файла .env:**

```
DB_NAME=<имя базы данных>
POSTGRES_USER=<логин для подключения к базе данных>
POSTGRES_PASSWORD=<пароль для подключения к БД (установите свой)>
DB_HOST=<название сервиса (контейнера)>
DB_PORT=<порт для подключения к БД>
```

4): Для сборки образов и создания контейнеров запустите следующую команду

```
docker-compose up -d 
```

5) Перейдите в контейнер под названием web:

```
docker-compose exec -it infra-backend-1 bash
```

6) В контейнере необходимо выполнить миграции, собрать статику и создать
   суперюзера:

```
python manage.py migrate
python manage.py createsuperuser
exit
```

Обратите внимание, что все команды необходимо выполнять в директории,
в которой расположен файл **manage.py**.

# Ресурсы Foodgram

**Для авторизованных пользователей:**

1. Доступна главная страница.
2. Доступна страница другого пользователя.
3. Доступна страница отдельного рецепта.
4. Доступна страница «Мои подписки».

- Можно подписаться и отписаться на странице рецепта.
- Можно подписаться и отписаться на странице автора.
- При подписке рецепты автора добавляются на страницу «Мои подписки» и
  удаляются оттуда при отказе от подписки.

5. Доступна страница «Избранное».

- На странице рецепта есть возможность добавить рецепт в список избранного и
  удалить его оттуда.
- На любой странице со списком рецептов есть возможность добавить рецепт в
  список избранного и удалить его оттуда.

6. Доступна страница «Список покупок».

- На странице рецепта есть возможность добавить рецепт в список покупок и
  удалить его оттуда.

- На любой странице со списком рецептов есть возможность добавить рецепт в
  список покупок и удалить его оттуда.

- Есть возможность выгрузить файл (.txt или .pdf) с перечнем и количеством
  необходимых ингредиентов для рецептов из «Списка покупок».

- Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается
  общее количество для каждого ингредиента.

7. Доступна страница «Создать рецепт».

- Есть возможность опубликовать свой рецепт.

- Есть возможность отредактировать и сохранить изменения в своём рецепте.

- Есть возможность удалить свой рецепт.

8. Доступна и работает форма изменения пароля.
9. Доступна возможность выйти из системы (разлогиниться).

**Для неавторизованных пользователей:**

1. Доступна главная страница.
2. Доступна страница отдельного рецепта.
3. Доступна и работает форма авторизации.
4. Доступна и работает система восстановления пароля.
5. Доступна и работает форма регистрации.

# ReDoc

Подробности об этом API, а так же примеры запросов можно найти в ReDoc
документации по адресу:

```
http://84.201.162.64/api/docs/redoc.html 
```

# Пример развернутого проекта

```
http://84.201.162.64/
```
**Адрес и учетные данные админки:**
```
Логин: Admin
email: Admin@mail.ru
Пароль: Admin1234
```

<img src="https://github.com/Bzhukov/foodgram-project-react/actions/workflows/main.yml/badge.svg">