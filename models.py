
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ShakhaLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100))
    district = db.Column(db.String(100))
    city = db.Column(db.String(100))
    basti = db.Column(db.String(100))
    shakha_name = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
