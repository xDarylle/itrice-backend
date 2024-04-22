from pydantic import BaseModel, StrictStr, StrictFloat, StrictBool

"""
This consists the different schemas for requests
"""

class LoginCredentials(BaseModel):
    email: StrictStr
    password: StrictStr
    remember: StrictBool

class ProductionData(BaseModel):
    irrigated: StrictFloat
    rainfeed: StrictFloat
    seedType: StrictStr

class UserData(BaseModel):
    name: StrictStr
    email: StrictStr
    password: StrictStr
    role: StrictStr