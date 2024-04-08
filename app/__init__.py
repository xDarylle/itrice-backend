from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# setup flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey123"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# import models and routes
from app import Models
from app.Routes import generate_routes
generate_routes(app)


# this is being executed before the first request 
with app.app_context():
    db.create_all()
    db.session.commit()

# this loads the user when user set remember me as true (default: remember_me = True)
@login_manager.user_loader
def load_user(user_id):
    return Models.User.query.get(int(user_id))