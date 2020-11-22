from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field is required')

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))  # param must be a tuple
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return item

        return {"message": "item not found"}, 404

    def post(self, name):
        if Item.find_by_name(name):
            return{'message': 'An item with name "{}" already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

        return item, 201

    def delete(self, name):
        pass

    def put(self, name):
        pass


class ItemList(Resource):
    def get(self):
        pass
