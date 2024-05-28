from flask_restful import Resource
from flask import request
from app.Models import Production
from app.Components.response import Response
from werkzeug.exceptions import NotFound
from flask_login import login_required
from app.configs.request_schema import ProductionData
from app.Components.validate_request import validate_request
import numpy as np
from sklearn.linear_model import LinearRegression

class LinearRegressionAPI(Resource):
    @login_required
    def get(self):
        pass