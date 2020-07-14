from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userN = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    passW = db.Column(db.String(80))
    isAdmin = db.Column(db.Boolean)