from flask import (Flask, render_template, abort, jsonify, request,
                   redirect, url_for)

from model import db, save_db

app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("welcome.html", cards=db)


@app.route("/projects/<string:project_name>")
def projects_view(project_name):
    if project_name == 'hollywood_divorces':
        return render_template("/projects/hollywood_divorces.html")
    elif project_name == 'disney_movies':
        return render_template("/projects/disney_movies.html")

    return render_template("/projects/projects_index.html")


@app.route("/card/<int:index>")
def card_view(index):
    try:
        card = db[index]
        return render_template("card.html",
                               card=card,
                               index=index,
                               max_index=len(db)-1)
    except IndexError:
        abort(404)


@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        # form submitted
        card = {"question": request.form['question'],
                "answer": request.form['answer']}
        db.append(card)
        save_db()
        return redirect(url_for('card_view', index=len(db)-1))
    else:
        return render_template("add_card.html")


@app.route("/remove_card/<int:index>", methods=["GET", "POST"])
def remove_card(index):
    if request.method == "POST":
        # form submitted

        del db[index]
        save_db()
        return redirect(url_for('welcome'))
    else:
        try:
            card = db[index]
            return render_template("delete_card.html",
                                   card=card)
        except IndexError:
            abort(404)


'''
API routes
'''


@ app.route('/api/card/')
def api_card_list():
    return jsonify(db)


@ app.route('/api/card/<int:index>')
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)
