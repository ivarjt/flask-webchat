"""
Admin Tool
"""

import sqlite3

database_file = 'database.db'
connection = sqlite3.connect(database_file)

cursor = connection.cursor()
create_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);
"""

cursor.execute(create_table_sql)

insert_data_sql = "INSERT INTO users (username, email, password) VALUES (?, ?, ?);"
#data_to_insert = [("user1", "user1@example.com", "lolipop"), ("user2", "user2@example.com", "losenord")]
data_to_insert = [("kokain", "cola@cola.cola", "cocacola")]


cursor.executemany(insert_data_sql, data_to_insert)
connection.commit()

connection.close()
