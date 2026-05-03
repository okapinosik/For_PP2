
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def init_db():
    """Создает таблицы, если их еще нет."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
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
                """
            )


def get_or_create_player(username):
    username = username.strip()[:50] or "Player"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO players(username)
                VALUES (%s)
                ON CONFLICT (username) DO UPDATE SET username = EXCLUDED.username
                RETURNING id;
                """,
                (username,),
            )
            return cur.fetchone()[0]


def save_result(username, score, level_reached):
    player_id = get_or_create_player(username)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO game_sessions(player_id, score, level_reached)
                VALUES (%s, %s, %s);
                """,
                (player_id, score, level_reached),
            )


def get_top_scores(limit=10):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    p.username,
                    gs.score,
                    gs.level_reached,
                    TO_CHAR(gs.played_at, 'YYYY-MM-DD HH24:MI') AS played_at
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC, gs.level_reached DESC, gs.played_at ASC
                LIMIT %s;
                """,
                (limit,),
            )
            return list(cur.fetchall())


def get_personal_best(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COALESCE(MAX(gs.score), 0)
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                WHERE p.username = %s;
                """,
                (username,),
            )
            return cur.fetchone()[0]
