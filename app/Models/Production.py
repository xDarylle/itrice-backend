from app import db
from app.Components import model
from sqlalchemy.sql import func
"""
This creates a table, and columns for Production.
"""


class Production(db.Model, model.Component):
    __tablename__ = "production"

    id = db.Column(db.Integer, primary_key=True)
    irrigated = db.Column(db.Float)
    rainfeed = db.Column(db.Float)
    seedType = db.Column(db.Text)
    dateCreated = db.Column(db.TIMESTAMP, server_default=func.now())
