from app import db
from flask_login import UserMixin
from app.Components import model

"""
This creates a table, and columns for user on the database.
"""


class User(UserMixin, db.Model, model.Component):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)

    # this checks if email exists in the database
    def create(self):
        if (self.query.filter_by(email=self.email).first()):
            raise ValueError("Email already taken!")

        db.session.add(self)
        db.session.commit()
