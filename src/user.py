import sqlite3
from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']

        if User.find_by_username(username) is not None:
            return { 'msg': 'Username already exists!' }, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        hash = generate_password_hash(data['password'])

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (username, hash))

        connection.commit()
        connection.close()

        return { 'success': True }, 201 
        

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username, ))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_userid(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id, ))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user