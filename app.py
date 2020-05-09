import os
from flask import Flask, render_template
from flask_jwt import JWT

from api_v1 import api as api_v1
from model import db, Fcuser

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api/v1')


@app.route('/')
def hello_world():
    return render_template("home.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "aaaabbbbb"

db.init_app(app)
db.app = app
db.create_all()


def authenticate(username, password):
    user = Fcuser.query.filter(Fcuser.userid == username).first()

    if user.password == password:
        return user


def identify(payload):
    print(payload)
    id = payload['identity']

    return Fcuser.query.filter(Fcuser.id == id).first()


jwt = JWT(app, authenticate, identify)

if __name__ == '__main__':
    app.run(debug=True)
