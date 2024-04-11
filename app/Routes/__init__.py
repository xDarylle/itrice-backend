from flask_restful import Api
from app.Routes.auth import Signup, Login, Logout
from app.Routes.production import ProductionAPI

def generate_routes(app):
    api = Api(app)
    
    api.add_resource(Signup, "/api/auth/signup")
    api.add_resource(Login, "/api/auth/login")
    api.add_resource(Logout, "/api/auth/logout")

    api.add_resource(ProductionAPI, "/api/production", "/api/production/<int:productionId>")
    
    