from pydantic import ValidationError
import json
from flask import request
from app.Components.response import Response

"""
The purpose of this is for validating requests body.
"""

def validate_request(JsonSchema):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                JsonSchema(**request.get_json())
                return func(*args, **kwargs)
            except ValidationError as e:
                params = [error['loc'][0] for error in json.loads(e.json())]
                param_list = ", ".join(params)
                return Response(
                    status=400,
                    message=f"Invalid or missing parameters: {param_list}"
                )
        return wrapper
    return decorator