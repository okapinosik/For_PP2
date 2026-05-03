# Snake PostgreSQL Edition

## 1. Установка библиотек

```bash
pip install -r requirements.txt
```

## 2. Создание базы PostgreSQL

Зайди в `psql` или pgAdmin и создай базу:

```sql
CREATE DATABASE snake_db;
```

Потом можно выполнить `schema.sql`, но игра также сама создаст таблицы при запуске.

## 3. Настройка подключения

Открой `config.py` и измени данные под свой PostgreSQL:

```python
DB_NAME = "snake_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
```

## 4. Запуск

```bash
python main.py
```

## Управление

- Стрелки или WASD — движение
- ESC — назад в меню во время игры

## Что реализовано

- Username entry
- Сохранение результата в PostgreSQL
- Top 10 leaderboard
- Personal best
- Poison food
- Weighted/disappearing food
- Speed boost, slow motion, shield
- Obstacles from level 3
- settings.json
- Main menu, game over, leaderboard, settings
