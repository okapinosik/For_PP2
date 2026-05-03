import os
import psycopg2
from config import host, user, password, db_name, port


os.environ["PGCLIENTENCODING"] = "UTF8"

connection = None

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port,
        options="-c client_encoding=UTF8"
    )

    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        print(f"Server version: {cursor.fetchone()}")

    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)

        print("[INFO] Tables created successfully")

except Exception as ex:
    print("[INFO] Error while working with PostgreSQL:")
    print(repr(ex))

finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")