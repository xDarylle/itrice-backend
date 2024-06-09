from flask_restful import Resource
from flask import request
from flask_login import login_required
from app.Models import User
from app.Components.response import Response
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash
from app.configs.request_schema import UserData
from app.Components.validate_request import validate_request


class ManageUsers(Resource):
    @login_required
    def get(self):
        page = int(request.args["page"])
        per_page = int(request.args["maxItem"])

        if not page:
            return Response(
                status=400,
                message="Page number not specified"
            )

        try:
            query = User.query.paginate(page=page, per_page=per_page)
            user_list = []
            for q in query:
                user = q.to_dict()
                del user["password"]
                user["dateCreated"] = user["dateCreated"].strftime(
                    "%Y-%m-%d %H:%M:%S")
                user_list.append(user)

            return Response(
                status=200,
                data=user_list
            )
        except Exception as e:
            return Response(
                status=500,
                message=str(e)
            )

    @login_required
    @validate_request(UserData)
    def post(self):
        req = request.get_json()

        name = req.get("name")
        email = req.get("email")
        password = req.get("password")
        role = req.get("role")

        try:
            user = User(
                name=name,
                email=email,
                password=generate_password_hash(password),
                role=role,
            )

            user.create()

            return Response(
                status=201,
                message="Successful registration"
            )
        except ValueError as e:
            return Response(
                status=409,
                message="Email already taken!"
            )
        except Exception as e:
            return Response(
                status=500,
                message=str(e)
            )

    @login_required
    @validate_request(UserData)
    def put(self, userId):
        try:
            user = User.query.get_or_404(userId)

            req = request.get_json()
            name = req.get("name")
            email = req.get("email")
            password = req.get("password")
            role = req.get("role")

            user.name = name
            user.email = email
            user.password = generate_password_hash(password)
            user.role = role

            user.update()

            return Response(
                status=200,
                message="Updated successfully"
            )
        except NotFound:
            return Response(
                status=404,
                message="User not found!"
            )
        except Exception as e:
            return Response(
                status=500,
                message=str(e)
            )

    @login_required
    def delete(self, userId):
        try:
            production = User.query.get_or_404(userId)
            production.delete()

            return Response(
                status=200,
                message="Successfully deleted"
            )
        except NotFound:
            return Response(
                status=404,
                message="User not found!"
            )
        except Exception as e:
            return Response(
                status=500,
                message=str(e)
            )
