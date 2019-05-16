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

@app.before_first_request
def create_tables():
    db.create_all()
 
jwt = JWT(app, authenticate, identity) # /auth

class Item(Resource):
    
    # @jwt_required()
    def get(self, name): 
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

    # @jwt_required()
    def delete(self, name):
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

class ItemList(Resource):
    def get(self):
        return { 'items': [item.json() for item in ItemModel.query.all()] }

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