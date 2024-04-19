from flask_restful import Resource
from flask import request
from app.Models import Production
from app.Components.response import Response
from werkzeug.exceptions import NotFound
from flask_login import login_required, current_user
from datetime import datetime


class ProductionAPI(Resource):
    @login_required
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
        page = int(request.args["page"])
        PER_PAGE = 12
        try:
            query = Production.query.paginate(page=page, per_page=PER_PAGE)
            production_list = []
            for q in query:
                q = q.to_dict()
                q["dateCreated"] = q["dateCreated"].strftime(
                    "%Y-%m-%d %H:%M:%S")
                production_list.append(q)

            return Response(
                status=200,
                data=production_list
            )
        except Exception as e:
            return Response(
                status=500,
                message=str(e)
            )

    @login_required
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
