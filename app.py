import os
from flask import Flask, render_template

from api_v1 import api as api_v1
from model import db

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api/v1')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/register')
def register():
    return render_template("register.html")


basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
db.app = app
db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
