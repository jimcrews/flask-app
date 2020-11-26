'''
 Debug with

 export FLASK_APP=app.py
 export FLASK_ENV=development
 export SECRET_KEY=mykey
 flask run

'''
from db import db
from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

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


db.init_app(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
