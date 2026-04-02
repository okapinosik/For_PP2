import psycopg2
import csv
import os
from config import host, user, password, db_name

def get_connection():
    return psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port="5432"
    )


def init_table():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50),
        phone_number VARCHAR(20) NOT NULL
    );
    """

    add_uq_person_sql = """
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1
            FROM pg_constraint
            WHERE conname = 'uq_person'
        ) THEN
            ALTER TABLE phonebook
            ADD CONSTRAINT uq_person UNIQUE (first_name, last_name);
        END IF;
    END $$;
    """

    add_uq_phone_sql = """
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1
            FROM pg_constraint
            WHERE conname = 'uq_phone'
        ) THEN
            ALTER TABLE phonebook
            ADD CONSTRAINT uq_phone UNIQUE (phone_number);
        END IF;
    END $$;
    """

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_sql)
                cur.execute(add_uq_person_sql)
                cur.execute(add_uq_phone_sql)
            conn.commit()
        print("[INFO] Таблица phonebook и ограничения готовы.")
    except Exception as e:
        print(f"[ERROR] Ошибка при создании таблицы: {e}")
        
def execute_sql_file(filename):
    if not os.path.exists(filename):
        print(f"[ERROR] Файл {filename} не найден.")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            sql_script = f.read()

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_script)
            conn.commit()

        print(f"[INFO] SQL из файла {filename} успешно выполнен.")
    except Exception as e:
        print(f"[ERROR] Ошибка при выполнении {filename}: {e}")


def initialize_database():
    init_table()
    execute_sql_file("functions.sql")
    execute_sql_file("procedures.sql")


def import_from_csv(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)

            with get_connection() as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        if len(row) < 3:
                            continue

                        fname = row[0].strip()
                        lname = row[1].strip()
                        phone = row[2].strip()

                        cur.execute(
                            "CALL insert_or_update_user(%s, %s, %s)",
                            (fname, lname, phone)
                        )
                conn.commit()

        print(f"[INFO] Импорт из {filename} завершён.")
    except Exception as e:
        print(f"[ERROR] Ошибка при импорте CSV: {e}")


def add_contact(fname, lname, phone):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL insert_or_update_user(%s, %s, %s)",
                    (fname, lname, phone)
                )
            conn.commit()

        print(f"[INFO] Контакт {fname} {lname} добавлен/обновлён.")
    except Exception as e:
        print(f"[ERROR] Не удалось добавить контакт: {e}")


def update_contact(contact_id, new_name=None, new_last=None, new_phone=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if new_name:
                    cur.execute(
                        "UPDATE phonebook SET first_name = %s WHERE id = %s",
                        (new_name, contact_id)
                    )
                if new_last:
                    cur.execute(
                        "UPDATE phonebook SET last_name = %s WHERE id = %s",
                        (new_last, contact_id)
                    )
                if new_phone:
                    cur.execute(
                        "UPDATE phonebook SET phone_number = %s WHERE id = %s",
                        (new_phone, contact_id)
                    )
            conn.commit()

        print(f"[INFO] Контакт с ID {contact_id} успешно обновлён.")
    except Exception as e:
        print(f"[ERROR] Не удалось обновить контакт: {e}")


def search_contacts(pattern):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
                results = cur.fetchall()

                if not results:
                    print("Ничего не найдено.")
                    return

                for row in results:
                    print(f"ID: {row[0]} | {row[1]} {row[2]} | Тел: {row[3]}")
    except Exception as e:
        print(f"[ERROR] Ошибка при поиске: {e}")


def insert_many_contacts():
    try:
        n = int(input("Сколько контактов хотите добавить? "))

        first_names = []
        last_names = []
        phones = []

        for i in range(n):
            print(f"\nКонтакт #{i + 1}")
            fname = input("Имя: ").strip()
            lname = input("Фамилия: ").strip()
            phone = input("Телефон: ").strip()

            first_names.append(fname)
            last_names.append(lname)
            phones.append(phone)

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CALL insert_many_users(%s, %s, %s, NULL)
                    """,
                    (first_names, last_names, phones)
                )

                invalid_rows = cur.fetchone()

            conn.commit()

        print("[INFO] Массовое добавление завершено.")

        if invalid_rows and invalid_rows[0]:
            print("Некорректные данные:")
            for item in invalid_rows[0]:
                print("-", item)
        else:
            print("Все записи корректны.")
    except ValueError:
        print("[ERROR] Нужно ввести число.")
    except Exception as e:
        print(f"[ERROR] Ошибка при массовой вставке: {e}")


def delete_contact(identifier):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_user_by_name_or_phone(%s)", (identifier,))
            conn.commit()

        print(f"[INFO] Удаление по значению '{identifier}' выполнено.")
    except Exception as e:
        print(f"[ERROR] Не удалось удалить контакт: {e}")


def show_all():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM phonebook ORDER BY id")
                results = cur.fetchall()

                if not results:
                    print("Телефонная книга пуста.")
                    return

                for row in results:
                    print(f"ID: {row[0]} | {row[1]} {row[2]} | Тел: {row[3]}")
    except Exception as e:
        print(f"[ERROR] Не удалось показать контакты: {e}")


def show_page(limit_value, offset_value):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_phonebook_page(%s, %s)",
                    (limit_value, offset_value)
                )
                results = cur.fetchall()

                if not results:
                    print("Нет данных для этой страницы.")
                    return

                for row in results:
                    print(f"ID: {row[0]} | {row[1]} {row[2]} | Тел: {row[3]}")
    except Exception as e:
        print(f"[ERROR] Ошибка при выводе страницы: {e}")


if __name__ == "__main__":
    initialize_database()

    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Импортировать контакты из CSV")
        print("2. Добавить новый контакт вручную")
        print("3. Найти контакт по шаблону")
        print("4. Обновить данные контакта по ID")
        print("5. Удалить контакт по имени / фамилии / номеру")
        print("6. Показать все номера")
        print("7. Добавить несколько контактов")
        print("8. Показать страницу контактов")
        print("0. Выход")

        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            filename = input("Введите имя CSV файла: ").strip()
            import_from_csv(filename)

        elif choice == "2":
            fname = input("Введите имя: ").strip()
            lname = input("Введите фамилию: ").strip()
            phone = input("Введите номер телефона: ").strip()
            add_contact(fname, lname, phone)

        elif choice == "3":
            pattern = input("Введите часть имени, фамилии или телефона: ").strip()
            print("\n--- Результаты поиска ---")
            search_contacts(pattern)

        elif choice == "4":
            cid = input("Введите ID контакта для редактирования: ").strip()
            print("Введите новые данные (или нажмите Enter, чтобы оставить без изменений):")
            n_name = input("Новое имя: ").strip()
            n_last = input("Новая фамилия: ").strip()
            n_phone = input("Новый телефон: ").strip()

            update_contact(
                cid,
                n_name if n_name else None,
                n_last if n_last else None,
                n_phone if n_phone else None
            )

        elif choice == "5":
            identifier = input("Введите имя / фамилию / full name / номер для удаления: ").strip()
            confirm = input(f"Вы уверены, что хотите удалить '{identifier}'? (да/нет): ").strip().lower()
            if confirm == "да":
                delete_contact(identifier)

        elif choice == "6":
            show_all()

        elif choice == "7":
            insert_many_contacts()

        elif choice == "8":
            try:
                limit_value = int(input("Введите LIMIT: "))
                offset_value = int(input("Введите OFFSET: "))
                print("\n--- Страница контактов ---")
                show_page(limit_value, offset_value)
            except ValueError:
                print("[ERROR] LIMIT и OFFSET должны быть числами")

        elif choice == "0":
            print("Завершение работы.")
            break

        else:
            print("Неверный ввод, попробуйте снова")