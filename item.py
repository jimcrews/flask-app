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

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

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
        try:
            Item.insert(item)
        except:
            return {"message": "An Error occurred inserting to database"}, 500

        return item, 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name =?"
        cursor.execute(query, (name,))  # params requires tuple
        connection.commit()
        connection.close()

        return {"message": "Item Deleted"}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item = Item.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {"message": "An Error occurred inserting to database"}, 500
        else:
            try:
                Item.update(updated_item)
            except:
                return {"message": "An Error occurred updating the database"}, 500

        return updated_item


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}
