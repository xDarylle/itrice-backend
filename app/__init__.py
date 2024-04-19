from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from flask_migrate import Migrate

# setup flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey123"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

    from app.Components.create_default_user import create_default_user
    create_default_user()

# this loads the user when user set remember me as true (default: remember_me = True)
@login_manager.user_loader
def load_user(user_id):
    return Models.User.query.get(int(user_id))
