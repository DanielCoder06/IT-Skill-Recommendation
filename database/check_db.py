import sqlite3

connection = sqlite3.connect("data/it_jobs.db")

cursor = connection.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table';
""")

tables = cursor.fetchall()

print("Các bảng trong database:")

for table in tables:
    print(table[0])

connection.close()