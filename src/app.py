from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from werkzeug.security import safe_str_cmp
from user import UserRegister
from item import ItemModel
import sqlite3  

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'keep it in ur pocket!'
api = Api(app)
 
jwt = JWT(app, authenticate, identity) # /auth
items = [
    { 'name': 'pen', 'price': 10 },
    { 'name': 'mouse', 'price': 20 }
]

class Item(Resource):
    
    # @jwt_required()
    def get(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name, ))
        # row = result.fetchone()
        # connection.close()
        # if row:
        #     return { 'item': { 'name': row[0], 'price': row[1] } }, 200
        # return { 'msg': 'Item not found!' }, 404  
        item = ItemModel.find_by_name(name)      
        if item:
            return item.json(), 200
        return { 'msg': 'Item not found!' }, 404  


    # @jwt_required()
    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return { 'msg': 'Item name already exists' }, 400

        req_body = request.get_json()
        price = float(req_body['price'])
        item = ItemModel(name, price)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred when inserting new item'}, 500
        
        return { 'success': True }, 201

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # data = request.get_json()
        # price = float(data['price'])

        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, ( name, ))
        # row = result.fetchone()

        # if row:
        #     return { 'msg': 'Item already exists!' }, 400

        # query_create = "INSERT INTO items (name, price) values (?, ?)"
        # cursor.execute(query_create, ( name, price ))
 
        # connection.commit()
        # connection.close()

        # return { 'success': True }, 201


    # @jwt_required()
    def delete(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, ( name, ))
        # row = result.fetchone()

        # if row is None:
        #     return { 'msg': 'Item does not exist!' }, 400

        # query_delete = "DELETE FROM items WHERE name=?"
        # cursor.execute(query_delete, ( name, ))

        # connection.commit()
        # connection.close()

        # return { 'success': True }, 200
        item = ItemModel.find_by_name(name)

        if item is None:
            return { 'msg': 'Item does not exist' }, 400

        try:
            item.delete_from_db()
        except:
            return {'msg': 'An error occurred when deleting item'}, 500

        return { 'success': True }, 200
        

    # @jwt_required()
    def put(self, name):
        item = ItemModel.find_by_name(name)

        req_body = request.get_json()
        price = float(req_body['price'])

        if item is None:
            item = ItemModel(name, price)
        else:
            item.price = price

        try:
            item.save_to_db() 
        except:
            return { 'msg': 'An error occurred when updating item' }, 500

        return item.json(), 200
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, ( name, ))
        # row = result.fetchone()

        # if row is None:
        #     return { 'msg': 'Item does not exist!' }, 400

        # data = request.get_json()
        # price = float(data['price'])

        # query_update = "UPDATE items SET price=? WHERE name=?"
        # cursor.execute(query_update, ( price, name ))

        # connection.commit()
        # connection.close()

        # return { 'success': True }, 200

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
    return 'homepage'

api.add_resource(Item, '/item/<string:name>')

api.add_resource(UserRegister, '/register')

api.add_resource(ItemList, '/items')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=3000, debug=True)