from flask_restful import Api
from app.Routes.auth import Login, Logout
from app.Routes.production import ProductionAPI
from app.Routes.users import ManageUsers
from app.Routes.dashboard import LinearRegressionMonthlyAPI, LinearRegressionYearlyAPI, QuarterlyAPI, MonthlySummationAPI


def generate_routes(app):
    api = Api(app)
    
    api.add_resource(Login, "/api/auth/login")
    api.add_resource(Logout, "/api/auth/logout")

    api.add_resource(ProductionAPI, "/api/production", "/api/production/<int:productionId>")
    api.add_resource(ManageUsers, "/api/users", "/api/users/<userId>")

    api.add_resource(LinearRegressionMonthlyAPI, "/api/dashboard/trend/month")
    api.add_resource(LinearRegressionYearlyAPI, "/api/dashboard/trend/year")

    api.add_resource(QuarterlyAPI, "/api/dashboard/quarterly")

    api.add_resource(MonthlySummationAPI, "/api/dashboard/summation")
    
    