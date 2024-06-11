from flask_restful import Resource
from flask import request
from app.Models import Production
from app.Components.response import Response
from werkzeug.exceptions import NotFound
from flask_login import login_required
from app.configs.request_schema import ProductionData
from app.Components.validate_request import validate_request
from sqlalchemy import desc
import math


class ProductionAPI(Resource):
    @login_required
    @validate_request(ProductionData)
    def post(self):
        req = request.get_json()

        irrigated = req.get("irrigated")
        rainfeed = req.get("rainfeed")
        seedType = req.get("seedType")

        try:
            production = Production(
                irrigated=irrigated,
                rainfeed=rainfeed,
                seedType=seedType,
            )

            production.create()

            return Response(
                status=201,
                message="Successfully added"
            )
        except Exception as e:
            return Response(
                status=500,
                message=str(e)
            )

    @login_required
    def get(self):
        args = request.args
        page = int(args["page"])
        per_page = int(args["maxItem"])

        if not page:
            return Response(
                status=400,
                message="Page number not specified"
            )

        try:
            query = []
            lastPage = None
            if args.get("seedType"):
                query = Production.query.filter(Production.seedType == args.get("seedType")).order_by(desc(Production.dateCreated)).paginate(
                    page=page, per_page=per_page)
                lastPage = math.ceil(len(Production.query.filter(
                    Production.seedType == args.get("seedType")).all()) / per_page)
            else:
                query = Production.query.order_by(
                    desc(Production.dateCreated)).paginate(page=page, per_page=per_page)
                lastPage = math.ceil(len(Production.query.all()) / per_page)

            production_list = []
            for q in query:
                q = q.to_dict()
                q["dateCreated"] = q["dateCreated"].strftime(
                    "%Y-%m-%d %H:%M:%S")
                q["irrigated"] = round(q["irrigated"], 2)
                q["rainfeed"] = round(q["rainfeed"], 2)
                production_list.append(q)

            return Response(
                status=200,
                data=production_list,
                maxPage=lastPage
            )
        except Exception as e:
            return Response(
                status=500,
                message=str(e)
            )

    @login_required
    @validate_request(ProductionData)
    def put(self, productionId):
        try:
            production = Production.query.get_or_404(productionId)

            req = request.get_json()
            irrigated = req.get("irrigated")
            rainfeed = req.get("rainfeed")
            seedType = req.get("seedType")

            production.irrigated = irrigated
            production.rainfeed = rainfeed
            production.seedType = seedType

            production.update()

            return Response(
                status=200,
                message="Updated successfully"
            )
        except NotFound:
            return Response(
                status=404,
                message="Production not found!"
            )
        except Exception as e:
            return Response(
                status=500,
                message=str(e)
            )

    @login_required
    def delete(self, productionId):
        try:
            production = Production.query.get_or_404(productionId)
            production.delete()

            return Response(
                status=200,
                message="Successfully deleted"
            )
        except NotFound:
            return Response(
                status=404,
                message="Production not found!"
            )
        except Exception as e:
            return Response(
                status=500,
                message=str(e)
            )
