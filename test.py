import sqlite3
# specifying database file
db = "./data/db.db"
db1 = "db1.db"

# connection object
connection = sqlite3.connect(db)
connection1 = sqlite3.connect(db1)

# cursor object
cursor = connection.cursor()
cursor1 = connection1.cursor()
statement = f"SELECT book_id FROM goodreads WHERE book_id = 1"
cursor.execute(statement)
tuples = cursor.fetchall()
book_id_lst = [row[0] for row in tuples]
book_id = book_id_lst[0]
print(book_id)