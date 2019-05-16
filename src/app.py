from flask import Flask, jsonify, request, Response
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from werkzeug.security import safe_str_cmp
from models.user import UserRegister
from models.item import ItemModel
from sqlalchemy.orm import validates
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
        
@app.route('/')
def home():
    return 'Home Page'

api.add_resource(UserRegister, '/register')

@app.route('/items', methods=['GET'])
def get_item_list():
    return jsonify({ 'items': [item.json() for item in ItemModel.query.all()] })

@app.route('/items', methods=['POST'])
@jwt_required()
def create_new_item():
    req_body = request.get_json()
    if 'price' not in req_body or not req_body['price']:
        return Response( '{ "msg": "Must provide price" }', status=400)
    if 'name' not in req_body or not req_body['name']:
        return Response( '{ "msg": "Must provide name" }', status=400 )

    name = req_body['name']
    price = req_body['price']

    item = ItemModel.find_by_name(name)

    if item:
        return Response('{"msg": "Item name already exists"}', status=400)

    item = ItemModel(name, price)

    try:
        item.save_to_db()
    except:
        return Response('{"msg": "An error occurred when inserting new item"}', status=500)
    
    return Response('{ "success": True }', status=201)

@app.route('/items/<string:name>', methods=['GET'])
def get_item_by_name(name):
    item = ItemModel.find_by_name(name)      
    if item:
        return Response(str(item.json()), status=200)
    return Response('{"msg": "Item not found"}', status=404 )

@app.route('/items/<string:name>', methods=['PUT'])
@jwt_required()
def update_item(name):
    req_body = request.get_json()
    if 'price' not in req_body or not req_body['price']:
        return Response( '{ "msg": "Must provide price" }', status=400)

    price = req_body['price']
    item = ItemModel.find_by_name(name)

    if item is None:
        item = ItemModel(name, price)
    else:
        item.price = price

    try:
        item.save_to_db() 
    except:
        return Response('{"msg": "An error occurred when updating item"}', status=500)
    return Response(str(item.json()), status=200)

@app.route('/items/<string:name>', methods=['DELETE'])
@jwt_required()
def delete_item(name):
    item = ItemModel.find_by_name(name)

    if item is None:
        return Response('{ "msg": "Item does not exist" }', status=400)

    try:
        item.delete_from_db()
    except:
        return Response('{"msg": "An error occurred when updating item"}', status=500)

    return Response('{ "success": True }', status=200)

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=3000, debug=True)