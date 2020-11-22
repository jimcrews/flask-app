import sqlite3

connection = sqlite3.connect('../data.db')
cur = connection.cursor()

create_users = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cur.execute(create_users)

create_items = "CREATE TABLE IF NOT EXISTS items (name test, price real)"
cur.execute(create_items)

cur.execute("INSERT INTO items VALUES ('test', 10.99)")

connection.commit()
connection.close()
