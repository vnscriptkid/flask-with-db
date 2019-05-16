import sqlite3
from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from db import db

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']

        if User.find_by_username(username) is not None:
            return { 'msg': 'Username already exists!' }, 400

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        hash = generate_password_hash(data['password'])

        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (username, hash))

        try:
            user = User(username, hash)
            user.save()
        except:
            return { 'msg': 'Error orcurred when creating new user' }, 500

        return { 'success': True }, 201

        # connection.commit()
        # connection.close()

        

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
        user = cls.query.filter_by(username = username).first()
        if user:
            return user.json()
        return None
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM users WHERE username=?"
        # result = cursor.execute(query, (username, ))
        # row = result.fetchone()
        # if row:
        #     user = cls(*row)
        # else:
        #     user = None
        # connection.close()
        # return user

    @classmethod
    def find_by_userid(cls, _id):
        user = cls.query.filter_by(id = _id).first()
        if user:
            return user.json()
        return None
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM users WHERE id=?"
        # result = cursor.execute(query, (_id, ))
        # row = result.fetchone()
        # if row:
        #     user = cls(*row)
        # else:
        #     user = None
        # connection.close()
        # return user