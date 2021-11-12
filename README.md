# Сравниваем вакансии программистов

Приложение позволяет вывести среднюю зарплату, которую предлагают программистам популярных языков.

Данные берутся из списка вакансий за последний месяц в московском регионе с сайтов `hh.ru` и `superjob.ru`.

## Как установить
### Загрузите зависимости
Должен быть установлен Python3. Используйте команду pip (или pip3, если возникает конфликт с Python2), чтобы установить зависимости:
```
pip install -r requirements.txt
```
### Подготовьте виртуальное окружение
Создайте файл `.env` в корневой директории проекта.

Для того чтобы воспользоваться данными с сайта `superjob.ru`, необходимо получить `secret_key`. Зарегистрируйтесь на [api.superjob.ru](https://api.superjob.ru/). Полученный `secret_key` необходимо сохранить в файле `.env`:
```
SUPERJOB_SECRET_KEY=your_secret_key
```
По умолчанию, в приложении использован набор популярных языков программирования на основании рейтинга `GitHub`.
Вы можете передать свой список языков, добавив их в виде простого списка в файл `.env`:
```
LANGUAGES="JavaScript","Java","Python","Ruby","PHP","C++","C#","Go","TypeScript"
```
Запустите приложение командой:
```
python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).