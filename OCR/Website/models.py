from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Doc(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    doc_name = db.Column(db.String(1000))
    image = db.Column(db.LargeBinary)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    


class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique= True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    docs = db.relationship('Doc')