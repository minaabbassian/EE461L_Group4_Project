import flask
from application import db


class User(db.Document):
    email = db.StringField()
    password = db.StringField()