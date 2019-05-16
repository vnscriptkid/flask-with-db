import sqlite3

class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @classmethod
    def get_item_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        if row:
            item = cls(*row)
        else:
            item = None
        connection.close()
        return item

    @classmethod
    def create_new_item(cls, name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items (name, price) values (?, ?)"
        result = cursor.execute(query, (name, price))
        row = result.fetchone()
        if row:
            item = cls(*row)
        else:
            item = None
        connection.close()
        return item
