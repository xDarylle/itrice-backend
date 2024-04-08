from flask_restful import Api
from app.Routes.auth import Signup, Login, Logout

def generate_routes(app):
    api = Api(app)
    
    api.add_resource(Signup, "/api/auth/signup")
    api.add_resource(Login, "/api/auth/login")
    api.add_resource(Logout, "/api/auth/logout")
    
    