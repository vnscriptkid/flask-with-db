import sqlite3
from code import *

# print(item.ItemModel.get_item_by_name('phone'))
one_item = item.ItemModel.get_item_by_name('phone')
# converted_one = {
#     'name': one_item['name'],
#     'price': one_item['price']
# }
print(one_item.name)

# connection = sqlite3.connect('data.db')

# cursor = connection.cursor()

# create_table = "CREATE TABLE users (id int, username text, password text)"
# cursor.execute(create_table)

# user = ('vnscriptkid', '123456')
# insert_table = "INSERT INTO users (username, password) VALUES (?, ?)"
# cursor.execute(insert_table, user)

# user_2 = ('someguy', '123456')
# insert_table = "INSERT INTO users (username, password) VALUES (?, ?)"
# cursor.execute(insert_table, user)

# users = [
#     ( 2, 'thanhnguyen', '654321' ),
#     ( 3, 'sleepyguy', '123456' )
# ]
# cursor.executemany(insert_table, users)

# insert_item_table = "INSERT INTO items (name, price) values (?, ?)"

# items = [
#     ( 'phone', 120.5 ),
#     ( 'headphone', 32.4 )
# ]
# cursor.executemany(insert_item_table, items)

# select_query = "SELECT * FROM users"
# for row in cursor.execute(select_query):
#     print(row)

# select_query = "SELECT * FROM items"
# for row in cursor.execute(select_query):
#     print(row)

# connection.commit()
# connection.close()