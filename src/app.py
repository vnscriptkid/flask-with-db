from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from werkzeug.security import safe_str_cmp
from user import UserRegister
import sqlite3  

app = Flask(__name__)
app.secret_key = 'keep it in ur pocket!'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth
items = [
    { 'name': 'pen', 'price': 10 },
    { 'name': 'mouse', 'price': 20 }
]

class Item(Resource):
    
    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()
        if row:
            return { 'item': { 'name': row[0], 'price': row[1] } }, 200
        return { 'msg': 'Item not found!' }, 404        

    @jwt_required()
    def post(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        data = request.get_json()
        price = float(data['price'])

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, ( name, ))
        row = result.fetchone()

        if row:
            return { 'msg': 'Item already exists!' }, 400

        query_create = "INSERT INTO items (name, price) values (?, ?)"
        cursor.execute(query_create, ( name, price ))
 
        connection.commit()
        connection.close()

        return { 'success': True }, 201


    # @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, ( name, ))
        row = result.fetchone()

        if row is None:
            return { 'msg': 'Item does not exist!' }, 400

        query_delete = "DELETE FROM items WHERE name=?"
        cursor.execute(query_delete, ( name, ))

        connection.commit()
        connection.close()

        return { 'success': True }, 200
        

    # @jwt_required()
    def put(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, ( name, ))
        row = result.fetchone()

        if row is None:
            return { 'msg': 'Item does not exist!' }, 400

        data = request.get_json()
        price = float(data['price'])

        query_update = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query_update, ( price, name ))

        connection.commit()
        connection.close()

        return { 'success': True }, 200

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        row = result.fetchone()
        item_list = []

        while (row is not None):
            item_list.append({ 'name': row[0], 'price': row[1] })
            row = result.fetchone()


        connection.commit()
        connection.close()

        return item_list, 200

@app.route('/')
def home():
    return 'homepage new'

api.add_resource(Item, '/item/<string:name>')

api.add_resource(UserRegister, '/register')

api.add_resource(ItemList, '/items')

app.run(port=3000, debug=True)