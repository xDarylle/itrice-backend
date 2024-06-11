from flask_restful import Resource
from flask import request
from app.Models import Production
from app.Components.response import Response
from werkzeug.exceptions import NotFound
from flask_login import login_required
from sqlalchemy import extract
from datetime import datetime
from app.Components.regression import predict
from app.Components.quarterly import quarterly
import pandas as pd
import calendar


class LinearRegressionAPI(Resource):
    @login_required
    def get(self):
        year = int(request.args["year"])
        if not year:
            year = datetime.now().year

        query = Production.query.filter(
            extract('year', Production.dateCreated) == year).all()
        data = [q.to_dict() for q in query]
        df = pd.DataFrame(data)

        irrigated = df.groupby(df['dateCreated'].dt.strftime('%m'))[
            'irrigated'].sum()
        irrigated_trend = predict(irrigated.index, irrigated.values)

        rainfeed = df.groupby(df['dateCreated'].dt.strftime('%m'))[
            'rainfeed'].sum()
        rainfeed_trend = predict(rainfeed.index, rainfeed.values)

        trend = {
            "irrigated": irrigated.values.tolist(),
            "irrigated_trend": irrigated_trend.tolist(),
            "rainfeed": rainfeed.values.tolist(),
            "rainfeed_trend": rainfeed_trend.tolist(),
            "month": [calendar.month_abbr[int(x)] for x in rainfeed.index]
        }

        return Response(
            status=200,
            data=trend
        )


class QuarterlyAPI(Resource):
    @login_required
    def get(self):
        args = request.args
        year = int(args["year"])

        query = None
        if args.get("seedType"):
            query = Production.query.filter(
                extract('year', Production.dateCreated) == year).filter(Production.seedType == args.get("seedType")).all()
        else:
            query = Production.query.filter(
                extract('year', Production.dateCreated) == year).all()

        if len(query) == 0:
            return Response(
                status=200,
                data=[]
            )

        data = [q.to_dict() for q in query]
        df = pd.DataFrame(data)

        irrigated = df.groupby(df['dateCreated'].dt.strftime('%m'))[
            'irrigated'].sum()
        quarterly_irrigated = quarterly(irrigated.values)
        quarterly_irrigated_trend = predict(
            [i for i in range(1, 5)], quarterly_irrigated)

        rainfeed = df.groupby(df['dateCreated'].dt.strftime('%m'))[
            'rainfeed'].sum()
        quarterly_rainfeed = quarterly(rainfeed.values)
        quarterly_rainfeed_trend = predict(
            [i for i in range(1, 5)], quarterly_rainfeed)

        return Response(
            status=200,
            data=[
                {"quarter": [i for i in range(1, 5)]},
                {"irrigated": [round(i, 2) for i in quarterly_irrigated]},
                {"irrigated_trend": [
                    round(i, 2) for i in quarterly_irrigated_trend.tolist()]},
                {"rainfeed": [round(i, 2) for i in quarterly_rainfeed]},
                {"rainfeed_trend": [round(i, 2)
                                    for i in quarterly_rainfeed_trend.tolist()]}
            ]
        )
