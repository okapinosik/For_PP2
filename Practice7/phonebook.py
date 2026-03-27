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
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        data = [row for row in reader]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                data
            )
        conn.commit()
    print(f"Импорт из {filename} завершен.")


def add_contact(fname, lname, phone):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
                    (fname, lname, phone)
                )
            conn.commit()
        print(f"[INFO] Контакт {fname} добавлен.")
    except Exception as e:
        print(f"[ERROR] Не удалось добавить контакт:{e}")


def update_contact(contact_id, new_name=None, new_last=None, new_phone=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if new_name:
                cur.execute("UPDATE phonebook SET first_name = %s WHERE id = %s", (new_name, contact_id))
            if new_last:
                cur.execute("UPDATE phonebook SET last_name = %s WHERE id = %s", (new_last, contact_id))
            if new_phone:
                cur.execute("UPDATE phonebook SET phone_number = %s WHERE id = %s", (new_phone, contact_id))
        conn.commit()
    print(f"Контакт с ID {contact_id} успешно обновлен.")


def search_contacts(query):
    with get_connection() as conn:
        with conn.cursor() as cur:
            sql_query = "SELECT * FROM phonebook WHERE first_name ILIKE %s OR last_name ILIKE %s OR phone_number LIKE %s"
            cur.execute(sql_query, (f'%{query}%', f'%{query}%', f'{query}%'))
            results = cur.fetchall()
            
            if not results:
                print("Ничего не найдено.")
            for row in results:
                print(f"ID: {row[0]} | {row[1]} {row[2]} | Тел: {row[3]}")

def delete_contact(identifier):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE first_name = %s OR phone_number = %s", (identifier, identifier))
        conn.commit()
        
    print(f"[INFO] Контакт {identifier} удален (если он существовал).")


def show_all():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook")
            results = cur.fetchall()

            if not results:
                print("Телефонная книга пуста.")
                return
            
            for row in results:
                print(f"ID: {row[0]} | {row[1]} {row[2]} | Тел: {row[3]}")
            

if __name__ == "__main__":
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Импортировать контакты из CSV")
        print("2. Добавить новый контакт вручную")
        print("3. Найти контакт (по имени или телефону)")
        print("4. Обновить данные контакта")
        print("5. Удалить контакт")
        print("6. Показать все номера")
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
            query = input("Введите имя или начало номера для поиска: ")
            print("\n--- Результаты поиска ---")
            search_contacts(query)

        elif choice == '4':
            cid = input("Введите ID контакта для редактирования: ")
            print("Введите новые данные (или нажмите Enter, чтобы оставить без изменений):")
            n_name = input("Новое имя: ")
            n_last = input("Новая фамилия: ")
            n_phone = input("Новый телефон: ")
            
            update_contact(cid, 
                   n_name if n_name else None, 
                   n_last if n_last else None, 
                   n_phone if n_phone else None)

        elif choice == '5':
            identifier = input("Введите имя или номер для удаления: ")
            confirm = input(f"Вы уверены, что хотите удалить {identifier}? (да/нет): ")
            if confirm.lower() == 'да':
                delete_contact(identifier)
                
        elif choice == '6':
            show_all()

        elif choice == '0':
            print("Завершение работы")
            break
        else:
            print("Неверный ввод, попробуйте снова.")