# PyHTTPD - Легковесный многопоточный HTTP-сервер на Python

## Описание  
**PyHTTPD** — это простой HTTP-сервер, реализованный на `Python`, поддерживающий **GET** и **HEAD** методы.  
Он использует **селекторы (selectors)** для эффективной обработки большого количества соединений.  

## Функциональность
- Обработка **GET** и **HEAD** запросов  
- **Многопоточная** обработка клиентов через `selectors`  
- Поддержка **Gzip-сжатия**  
- **Кеширование** файлов для повышения производительности  
- **Журналирование** запросов и ошибок  

## Установка

1. Клонирование репозитория:

```sh
git clone git@github.com:therealalexmois/pyhttpd.git
cd warehouse-management
```

2. Создание виртуального окружения:

```sh
eval $(poetry env activate)
```

3. Установка зависимостей:

```sh
poetry install
```

4. Запуск сервера:

```sh
python -m pyhttpd/server
```

Сервер стартует по адресу: http://localhost:8080

## Структура проекта

```sh
pyhttpd/
├── server.py          # Основной сервер
├── config.py          # Конфигурация сервера
├── logger.py          # Логирование
├── www/               # Статические файлы (index.html, 404.html)
├── tests/             # Тесты (нагрузочное тестирование)
├── README.md          # Документация
└── requirements.txt   # Зависимости (если есть)
```

## Нагрузочное тестирование

Apache Benchmark (ab)

```sh
ab -n 1000 -c 10 http://127.0.0.1:8080/index.html
```

WRK

```sh
wrk -t12 -c400 -d30s http://127.0.0.1:8080/index.html
```

## Конфигурация

Файл config.py содержит настройки:

```sh
HOST = "localhost"
PORT = 8080
DOCUMENT_ROOT = "./www"
LOG_FILE = "server.log"
LOG_LEVEL = "INFO"
```
