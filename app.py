'''
 Debug with

 export FLASK_APP=app.py
 export FLASK_ENV=development
 flask run

'''
from flask import (Flask, render_template, abort, request,
                   redirect, url_for)

from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.config.from_pyfile('config.py')

api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/projects/<string:project_name>")
def projects_view(project_name):
    if project_name == 'hollywood_divorces':
        return render_template("/projects/hollywood_divorces.html")
    elif project_name == 'disney_movies':
        return render_template("/projects/disney_movies.html")

    return render_template("/projects/projects_index.html")


'''
API routes
'''

items = []


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field is required')

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return{'message': 'An item with name "{}" already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)

        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
