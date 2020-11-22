import sqlite3
from flask_restful import Resource, reqparse


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users where username=?'
        result = cursor.execute(query, (username,))  # param must be a tuple
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users where id=?'
        result = cursor.execute(query, (_id,))  # param must be a tuple
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field is required')
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field is required')

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        connection = sqlite3.connect('data.db')
        curser = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"  # id is auto increment
        curser.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created succesfully"}, 201
