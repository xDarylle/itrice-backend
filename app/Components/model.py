from app import db
"""
The purpose of this is to handle the creating, updating, and deleting of objects created from the models
"""
class Component():
    def create(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()