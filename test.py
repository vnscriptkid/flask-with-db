import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# create_table = "CREATE TABLE users (id int, username text, password text)"
# cursor.execute(create_table)

# user = (1, 'vnscriptkid', '123456')
# insert_table = "INSERT INTO users VALUES (?, ?, ?)"
# cursor.execute(insert_table, user)

# users = [
#     ( 2, 'thanhnguyen', '654321' ),
#     ( 3, 'sleepyguy', '123456' )
# ]
# cursor.executemany(insert_table, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()