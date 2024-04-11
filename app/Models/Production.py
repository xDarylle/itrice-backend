from app import db
from app.Components import model

"""
This creates a table, and columns for Production.
"""


class Production(db.Model, model.Component):
    __tablename__ = "production"

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref("production"))
    irrigated = db.Column(db.Float)
    rainfeed = db.Column(db.Float)
    seedType = db.Column(db.Text)
    #date = db.Column(db.TIMESTAMP)
