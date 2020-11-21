'''
 Debug with

 export FLASK_APP=app.py
 export FLASK_ENV=development
 flask run
'''
from flask import (Flask, render_template, abort, request,
                   redirect, url_for)

from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


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
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item': None}, 404

    def post(self, name):
        data = request.get_json()
        item = {
            'name': name,
            'price': data['price']
        }
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
