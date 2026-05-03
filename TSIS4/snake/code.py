import psycopg2
from config import host, user, password, db_name, port


def get_connection():
    return psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )


class DBManager:
    def save_result(self, username, score, level):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO players (username)
                    VALUES (%s)
                    ON CONFLICT (username) DO UPDATE SET username = EXCLUDED.username
                    RETURNING id;
                    """,
                    (username,)
                )

                player_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO game_sessions (player_id, score, level_reached)
                    VALUES (%s, %s, %s);
                    """,
                    (player_id, score, level)
                )

            conn.commit()
            print(f"[DB] Saved: {username} - {score}")

        except Exception as e:
            conn.rollback()
            print(f"[DB] Error saving: {e}")

        finally:
            conn.close()

    def get_top_10(self):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        p.username,
                        s.score,
                        s.level_reached,
                        TO_CHAR(s.played_at, 'YYYY-MM-DD HH24:MI')
                    FROM game_sessions s
                    JOIN players p ON s.player_id = p.id
                    ORDER BY s.score DESC, s.level_reached DESC, s.played_at ASC
                    LIMIT 10;
                """
                cursor.execute(query)
                return cursor.fetchall()

        except Exception as e:
            print(f"[DB] Error fetching top 10: {e}")
            return []

        finally:
            conn.close()

    def get_personal_best(self, username):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT COALESCE(MAX(s.score), 0)
                    FROM game_sessions s
                    JOIN players p ON s.player_id = p.id
                    WHERE p.username = %s;
                """
                cursor.execute(query, (username,))
                return cursor.fetchone()[0]

        except Exception as e:
            print(f"[DB] Error fetching personal best: {e}")
            return 0

        finally:
            conn.close()