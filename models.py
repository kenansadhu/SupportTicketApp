# models.py
from extensions import db

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_category = db.Column(db.String(100))
    user_email = db.Column(db.String(120))
    problem_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

class ProblemType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
