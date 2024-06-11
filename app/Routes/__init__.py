from flask_restful import Api
from app.Routes.auth import Login, Logout
from app.Routes.production import ProductionAPI
from app.Routes.users import ManageUsers
from app.Routes.dashboard import LinearRegressionAPI, QuarterlyAPI


def generate_routes(app):
    api = Api(app)
    
    api.add_resource(Login, "/api/auth/login")
    api.add_resource(Logout, "/api/auth/logout")

    api.add_resource(ProductionAPI, "/api/production", "/api/production/<int:productionId>")
    api.add_resource(ManageUsers, "/api/users", "/api/users/<userId>")

    api.add_resource(LinearRegressionAPI, "/api/dashboard/trend")
    api.add_resource(QuarterlyAPI, "/api/dashboard/quarterly")
    
    