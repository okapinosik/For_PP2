import psycopg2
from connect import connect

conn = connect()
cursor = conn.cursor()


with open("TSIS/TSIS1/functions.sql", 'r', encoding='utf-8') as f:
    functions_sql = f.read()
    cursor.execute(functions_sql)
    print("Successfuly run functions.sql")


with open("TSIS/TSIS1/procedures.sql", 'r', encoding='utf-8') as f:
    procedures_sql = f.read()
    cursor.execute(procedures_sql)
    print("Successfuly run procedures.sql")

conn.commit()
cursor.close()
conn.close()