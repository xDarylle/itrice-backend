from flask_restful import Resource
from flask import request
from flask_login import login_required, logout_user, login_user
from app.Models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.Components.response import Response
from werkzeug.exceptions import NotFound


class Signup(Resource):
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


class Login(Resource):
    def post(self):
        req = request.get_json()

        email = req.get("email")
        password = req.get("password")
        remember = req.get("remember")

        try:
            user = User.query.filter_by(email=email).first_or_404()

            if not check_password_hash(user.password, password):
                raise ValueError("Invalid Password")

            login_user(user, remember=remember)

            return Response(
                status=200,
                message="Successful login"
            )
        except NotFound:
            return Response(
                status=404,
                message="User does not exist"
            )
        except ValueError as e:
            return Response(
                status=401,
                message="Invalid password"
            )
        except Exception as e:
            return Response(
                status=500,
                message=str(e)
            )


class Logout(Resource):
    @login_required
    def post(self):
        try:
            logout_user()

            return Response(
                status=200,
                message="Successful logout"
            )
        except Exception as e:
            return Response(
                status=500,
                message=str(e)
            )
