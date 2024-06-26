from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from flask_migrate import Migrate
import pandas as pd


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
    from app.Models.Production import Production
    create_default_user()

    ### Import data to database
    if not Production.query.first():
        c = input("Import data (y/n): ")
        if(c == 'y'):
            from app.Components.import_data import import_data
            print("Reading data...")
            df = pd.read_csv("data/iloilo.csv")
            print("Importing data. Please wait...")
            for index, row in df.iterrows():
                date = row['date']
                irrigated = row['irrigated']
                rainfeed = row['rainfeed']
                seed_type = row['seed_type']
                import_data(date, irrigated, rainfeed, seed_type)
            print("Importing done!")
        

# this loads the user when user set remember me as true (default: remember_me = True)
@login_manager.user_loader
def load_user(user_id):
    return Models.User.query.get(int(user_id))
