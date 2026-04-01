import psycopg2
import csv
from config import host, user, password, db_name

def get_connection():
    return psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port="5432"
    )


def import_from_csv(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            data = [row for row in reader]

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(
                    """
                    INSERT INTO phonebook (first_name, last_name, phone_number)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    data
                )
            conn.commit()

        print(f"Импорт из {filename} завершен.")
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

        print(f"[INFO] Контакт {fname} {lname} добавлен/обновлен.")
    except Exception as e:
        print(f"[ERROR] Не удалось добавить/обновить контакт: {e}")


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

        print(f"Контакт с ID {contact_id} успешно обновлен.")
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
                    CALL insert_many_users(%s, %s, %s, %s)
                    """,
                    (first_names, last_names, phones, [])
                )
            conn.commit()

        print("[INFO] Массовое добавление завершено.")
        print("Если были некорректные номера, procedure должна вернуть их в PostgreSQL.")
        print("Для полного вывода invalid data иногда удобнее смотреть через pgAdmin / psql.")
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
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Импортировать контакты из CSV")
        print("2. Добавить новый контакт вручную (procedure)")
        print("3. Найти контакт по шаблону (function)")
        print("4. Обновить данные контакта по ID")
        print("5. Удалить контакт по имени / фамилии / телефону (procedure)")
        print("6. Показать все номера")
        print("7. Добавить несколько контактов (procedure)")
        print("8. Показать страницу контактов (LIMIT/OFFSET function)")
        print("0. Выход")

        choice = input("\nВыберите действие: ")

        if choice == '1':
            filename = input("Введите имя CSV файла: ")
            import_from_csv(filename)

        elif choice == '2':
            fname = input("Введите имя: ")
            lname = input("Введите фамилию: ")
            phone = input("Введите номер телефона: ")
            add_contact(fname, lname, phone)

        elif choice == '3':
            pattern = input("Введите часть имени, фамилии или телефона: ")
            print("\n--- Результаты поиска ---")
            search_contacts(pattern)

        elif choice == '4':
            cid = input("Введите ID контакта для редактирования: ")
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

        elif choice == '5':
            identifier = input("Введите имя / фамилию / full name / номер для удаления: ")
            confirm = input(f"Вы уверены, что хотите удалить '{identifier}'? (да/нет): ")
            if confirm.lower() == 'да':
                delete_contact(identifier)

        elif choice == '6':
            show_all()

        elif choice == '7':
            insert_many_contacts()

        elif choice == '8':
            try:
                limit_value = int(input("Введите LIMIT: "))
                offset_value = int(input("Введите OFFSET: "))
                print("\n--- Страница контактов ---")
                show_page(limit_value, offset_value)
            except ValueError:
                print("[ERROR] LIMIT и OFFSET должны быть числами.")

        elif choice == '0':
            print("Завершение работы.")
            break

        else:
            print("Неверный ввод, попробуйте снова.")