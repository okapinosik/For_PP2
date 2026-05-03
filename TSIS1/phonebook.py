import psycopg2
import csv
import json
import os
from datetime import datetime
from config import host, user, password, db_name


def get_connection():
    return psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port="5432"
    )


def execute_sql_file(filename):
    if not os.path.exists(filename):
        print(f"[ERROR] Файл {filename} не найден.")
        return

    try:
        with open(filename, "r", encoding="utf-8") as file:
            sql = file.read()

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()

        print(f"[INFO] {filename} выполнен успешно.")
    except Exception as e:
        print(f"[ERROR] Ошибка при выполнении {filename}: {e}")


def initialize_database():
    print("Текущая папка:", os.getcwd())
    print("Файлы:", os.listdir())
    execute_sql_file("schema.sql")
    execute_sql_file("functions.sql")
    execute_sql_file("procedures.sql")


def parse_date(value):
    value = value.strip()
    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        print("[ERROR] Дата должна быть в формате YYYY-MM-DD.")
        return None


def print_contact(row):
    print(
        f"ID: {row[0]} | "
        f"{row[1]} {row[2] or ''} | "
        f"Email: {row[3] or '-'} | "
        f"Birthday: {row[4] or '-'} | "
        f"Group: {row[5] or '-'} | "
        f"Phones: {row[6] or '-'}"
    )


def add_contact():
    first_name = input("Имя: ").strip()
    last_name = input("Фамилия: ").strip()
    email = input("Email: ").strip()
    birthday = parse_date(input("Birthday YYYY-MM-DD: "))
    group_name = input("Group Family/Work/Friend/Other: ").strip() or "Other"
    phone = input("Телефон: ").strip()
    phone_type = input("Тип телефона home/work/mobile: ").strip()

    if phone_type not in ("home", "work", "mobile"):
        print("[ERROR] Тип должен быть home, work или mobile.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL insert_or_update_contact(%s, %s, %s, %s, %s, %s, %s)",
                    (
                        first_name,
                        last_name,
                        email,
                        birthday,
                        group_name,
                        phone,
                        phone_type
                    )
                )
            conn.commit()

        print("[INFO] Контакт добавлен или обновлён.")
    except Exception as e:
        print(f"[ERROR] Не удалось добавить контакт: {e}")


def add_phone_to_contact():
    contact_name = input("Введите имя или полное имя контакта: ").strip()
    phone = input("Введите новый номер: ").strip()
    phone_type = input("Тип телефона home/work/mobile: ").strip()

    if phone_type not in ("home", "work", "mobile"):
        print("[ERROR] Тип должен быть home, work или mobile.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL add_phone(%s, %s, %s)",
                    (contact_name, phone, phone_type)
                )
            conn.commit()

        print("[INFO] Телефон добавлен.")
    except Exception as e:
        print(f"[ERROR] Не удалось добавить телефон: {e}")


def move_contact_to_group():
    contact_name = input("Введите имя или полное имя контакта: ").strip()
    group_name = input("Введите новую группу: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL move_to_group(%s, %s)",
                    (contact_name, group_name)
                )
            conn.commit()

        print("[INFO] Контакт перемещён в группу.")
    except Exception as e:
        print(f"[ERROR] Не удалось переместить контакт: {e}")


def search_contacts_console():
    query = input("Введите имя, телефон или email для поиска: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_contacts(%s)", (query,))
                results = cur.fetchall()

        if not results:
            print("Ничего не найдено.")
            return

        for row in results:
            print_contact(row)
    except Exception as e:
        print(f"[ERROR] Ошибка поиска: {e}")


def filter_by_group():
    group_name = input("Введите группу Family/Work/Friend/Other: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_page(%s, %s, %s, %s)",
                    (100, 0, "id", group_name)
                )
                results = cur.fetchall()

        if not results:
            print("В этой группе нет контактов.")
            return

        for row in results:
            print_contact(row)
    except Exception as e:
        print(f"[ERROR] Ошибка фильтрации: {e}")


def show_sorted_contacts():
    print("Сортировка:")
    print("1. По имени")
    print("2. По дню рождения")
    print("3. По дате добавления")

    choice = input("Выберите: ").strip()

    sort_map = {
        "1": "name",
        "2": "birthday",
        "3": "date_added"
    }

    sort_by = sort_map.get(choice, "id")

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_page(%s, %s, %s, %s)",
                    (100, 0, sort_by, None)
                )
                results = cur.fetchall()

        if not results:
            print("Телефонная книга пустая.")
            return

        for row in results:
            print_contact(row)
    except Exception as e:
        print(f"[ERROR] Ошибка сортировки: {e}")


def paginated_navigation():
    limit_value = 5
    offset_value = 0
    sort_by = "id"

    while True:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM get_contacts_page(%s, %s, %s, %s)",
                        (limit_value, offset_value, sort_by, None)
                    )
                    results = cur.fetchall()

            print("\n--- Страница контактов ---")

            if not results:
                print("Нет данных на этой странице.")
            else:
                for row in results:
                    print_contact(row)

            command = input("\nnext / prev / quit: ").strip().lower()

            if command == "next":
                offset_value += limit_value
            elif command == "prev":
                offset_value = max(0, offset_value - limit_value)
            elif command == "quit":
                break
            else:
                print("Неизвестная команда.")
        except Exception as e:
            print(f"[ERROR] Ошибка пагинации: {e}")
            break


def export_to_json():
    filename = input("Введите имя JSON файла для экспорта: ").strip()

    if not filename.endswith(".json"):
        filename += ".json"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_page(%s, %s, %s, %s)", (100000, 0, "id", None))
                rows = cur.fetchall()

        contacts = []

        for row in rows:
            contacts.append({
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "birthday": str(row[4]) if row[4] else None,
                "group": row[5],
                "phones": row[6]
            })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4, ensure_ascii=False)

        print(f"[INFO] Экспорт завершён: {filename}")
    except Exception as e:
        print(f"[ERROR] Ошибка экспорта JSON: {e}")


def import_from_json():
    filename = input("Введите имя JSON файла: ").strip()

    if not os.path.exists(filename):
        print("[ERROR] Файл не найден.")
        return

    try:
        with open(filename, "r", encoding="utf-8") as file:
            contacts = json.load(file)

        with get_connection() as conn:
            with conn.cursor() as cur:
                for contact in contacts:
                    first_name = contact.get("first_name")
                    last_name = contact.get("last_name")
                    email = contact.get("email")
                    birthday = contact.get("birthday")
                    group_name = contact.get("group") or "Other"

                    existing = None
                    cur.execute(
                        """
                        SELECT id FROM contacts
                        WHERE first_name = %s AND last_name = %s
                        """,
                        (first_name, last_name)
                    )
                    existing = cur.fetchone()

                    if existing:
                        action = input(
                            f"Контакт {first_name} {last_name} уже существует. "
                            f"skip/overwrite? "
                        ).strip().lower()

                        if action == "skip":
                            continue

                    phones_text = contact.get("phones")

                    if phones_text:
                        first_phone = phones_text.split(",")[0].strip()

                        if "(" in first_phone:
                            phone = first_phone.split("(")[0].strip()
                            phone_type = first_phone.split("(")[1].replace(")", "").strip()
                        else:
                            phone = first_phone
                            phone_type = "mobile"
                    else:
                        phone = input(f"Введите телефон для {first_name}: ").strip()
                        phone_type = "mobile"

                    cur.execute(
                        "CALL insert_or_update_contact(%s, %s, %s, %s, %s, %s, %s)",
                        (
                            first_name,
                            last_name,
                            email,
                            birthday,
                            group_name,
                            phone,
                            phone_type
                        )
                    )

            conn.commit()

        print("[INFO] Импорт JSON завершён.")
    except Exception as e:
        print(f"[ERROR] Ошибка импорта JSON: {e}")


def import_from_csv():
    filename = input("Введите имя CSV файла: ").strip()

    if not os.path.exists(filename):
        print("[ERROR] CSV файл не найден.")
        return

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            with get_connection() as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        first_name = row.get("first_name", "").strip()
                        last_name = row.get("last_name", "").strip()
                        email = row.get("email", "").strip()
                        birthday = row.get("birthday", "").strip() or None
                        group_name = row.get("group", "Other").strip()
                        phone = row.get("phone", "").strip()
                        phone_type = row.get("phone_type", "mobile").strip()

                        if phone_type not in ("home", "work", "mobile"):
                            phone_type = "mobile"

                        if not first_name or not phone:
                            continue

                        cur.execute(
                            "CALL insert_or_update_contact(%s, %s, %s, %s, %s, %s, %s)",
                            (
                                first_name,
                                last_name,
                                email,
                                birthday,
                                group_name,
                                phone,
                                phone_type
                            )
                        )

                conn.commit()

        print("[INFO] CSV импорт завершён.")
    except Exception as e:
        print(f"[ERROR] Ошибка CSV импорта: {e}")


def delete_contact():
    value = input("Введите имя / фамилию / full name / телефон: ").strip()
    confirm = input(f"Удалить '{value}'? да/нет: ").strip().lower()

    if confirm != "да":
        print("Удаление отменено.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact_by_name_or_phone(%s)", (value,))
            conn.commit()

        print("[INFO] Удаление выполнено.")
    except Exception as e:
        print(f"[ERROR] Ошибка удаления: {e}")


def show_all_contacts():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_page(%s, %s, %s, %s)",
                    (100000, 0, "id", None)
                )
                results = cur.fetchall()

        if not results:
            print("Телефонная книга пустая.")
            return

        for row in results:
            print_contact(row)
    except Exception as e:
        print(f"[ERROR] Не удалось показать контакты: {e}")


if __name__ == "__main__":
    initialize_database()

    while True:
        print("\n--- Extended PhoneBook Menu ---")
        print("1. Добавить / обновить контакт")
        print("2. Добавить дополнительный телефон контакту")
        print("3. Переместить контакт в группу")
        print("4. Поиск по имени / телефону / email")
        print("5. Фильтр по группе")
        print("6. Сортировка контактов")
        print("7. Пагинация next / prev / quit")
        print("8. Экспорт в JSON")
        print("9. Импорт из JSON")
        print("10. Импорт из CSV")
        print("11. Показать все контакты")
        print("12. Удалить контакт")
        print("0. Выход")

        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            add_phone_to_contact()
        elif choice == "3":
            move_contact_to_group()
        elif choice == "4":
            search_contacts_console()
        elif choice == "5":
            filter_by_group()
        elif choice == "6":
            show_sorted_contacts()
        elif choice == "7":
            paginated_navigation()
        elif choice == "8":
            export_to_json()
        elif choice == "9":
            import_from_json()
        elif choice == "10":
            import_from_csv()
        elif choice == "11":
            show_all_contacts()
        elif choice == "12":
            delete_contact()
        elif choice == "0":
            print("Завершение работы.")
            break
        else:
            print("Неверный ввод.")