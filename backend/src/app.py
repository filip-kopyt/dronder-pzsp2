from flask import Flask

import auth
from db import DATABASE_URL, db


app = Flask(__name__, instance_relative_config=True)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.register_blueprint(auth.bp)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "<p>Hi, World!</p>"
