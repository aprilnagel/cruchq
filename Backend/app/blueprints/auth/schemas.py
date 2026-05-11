from marshmallow import Schema, fields
from app.extensions import ma
from app.models import Users

#ONLY INPUT SCHEMAS FOR SIGNUP AND LOGIN

#___________SIGNUP SCHEMA____________
#used for:
# - validating incoming data for user registration
# - serializing user data for responses (if needed)
# - deserializing data from requests into Python objects

# not using SQL

class SignupSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)

    phone = fields.String(required=False)
    city = fields.String(required=False)
    state_province = fields.String(required=False)
    country = fields.String(required=False)
    continent = fields.String(required=False)
    bio = fields.String(required=False)
    dob = fields.Date(required=False)

    gender_id = fields.Integer(required=False)
    pronouns_id = fields.Integer(required=False)
    
    roles = fields.List(fields.Integer(), required=False)
    
        
signup_schema = SignupSchema()

#___________LOGIN SCHEMA____________
#used for:
# - validating and deserializing incoming data for user login (email and password). json to python data
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    
login_schema = LoginSchema()