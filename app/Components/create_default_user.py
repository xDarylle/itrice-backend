from app.Models import User
from werkzeug.security import generate_password_hash
from app.configs.default import NAME, EMAIL, PASSWORD, ROLE


def create_default_user():
    user = User.query.filter_by(email=EMAIL).first()
    if (user):
        user.delete()

    user = User(
        name=NAME,
        email=EMAIL,
        password=generate_password_hash(PASSWORD),
        role=ROLE,
    )

    user.create()
