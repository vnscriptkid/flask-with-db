from werkzeug.security import generate_password_hash
from flask import request
from flask_restful import Resource
from db import db

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        if ('username' not in data or not data['username']):
            return { 'msg': 'Must provide username' }, 400

        if ('password' not in data or not data['password']):
            return { 'msg': 'Must provide password' }, 400

        username = data['username']

        if User.find_by_username(username) is not None:
            return { 'msg': 'Username already exists!' }, 400

        hash = generate_password_hash(data['password'])

        try:
            user = User(username, hash)
            user.save_to_db()
        except:
            return { 'msg': 'Error orcurred when creating new user' }, 500

        return { 'success': True }, 201

class User(db.Model):
    __tablename__ = 'users'    

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(256))
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_userid(cls, _id):
        return cls.query.filter_by(id = _id).first()