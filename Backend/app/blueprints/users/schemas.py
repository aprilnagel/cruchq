from marshmallow import Schema, fields, validate
from app.extensions import ma
from app.models import Users
from datetime import date

# load_instance=True makes Marshmallow create SQLAlchemy model objects when loading data; load_instance=False makes it return plain dictionaries. For input or public schemas, always use load_instance=False to avoid unsafe auto‑magic. For output schemas, you can use load_instance=True if you want to work with model instances, but it's often safer to keep it False and just return dictionaries to the frontend.  

#_____________USER SCHEMA_____________________
#used for: 
    #  serializing and deserializing user data - meaning sending back to the  frontend.
    #  /me endpoint, when the backend needs to send user info to the frontend

#SERIALIZATION (dump) excludes password for security reasons
#BACKEND OUTPUT SCHEMA - this is what we send back to the frontend when we want to provide user information. It includes all the fields that are relevant for the frontend to know about the user, but excludes sensitive information like the password.

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Users
        load_instance = True
        include_fk = False
        include_relationships = False

    id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    email = ma.auto_field()
    phone = ma.auto_field()
    city = ma.auto_field()
    state_province = ma.auto_field()
    country = ma.auto_field()
    continent = ma.auto_field()
    bio = ma.auto_field()
    dob = ma.auto_field()
    profile_picture_url = ma.auto_field()
    system_role = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

    #CONVERTING FOREIGN KEYS TO READABLE STRINGS
        # - The Users table stores only gender_id and pronouns_id, so the UserSchema uses fields.Method() to follow the relationship and return the readable label (gender_name or pronoun_label) instead of the raw ID.
    gender = fields.Method("get_gender")
    pronouns = fields.Method("get_pronouns")


    def get_gender(self, obj):
        return obj.gender.gender_name if obj.gender else None

    def get_pronouns(self, obj):
        return obj.pronouns.pronoun_label if obj.pronouns else None
    
user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserPublicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Users
        load_instance = False
        include_fk = False
        include_relationships = False

    id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    profile_picture_url = ma.auto_field()
    age = fields.Method("calculate_age")
    city = ma.auto_field()
    state_province = ma.auto_field()
    country = ma.auto_field()
    continent = ma.auto_field()
    gender = fields.Method("get_gender")
    pronouns = fields.Method("get_pronouns")
    tour_count = fields.Method("get_tour_count")
    roles = fields.Method("get_roles")

    def calculate_age(self, obj):
        if obj.dob:
            today = date.today()
            return (
                today.year
                - obj.dob.year
                - ((today.month, today.day) < (obj.dob.month, obj.dob.day))
            )
        return None

    def get_tour_count(self, obj):
        return len(obj.tour_crew) if obj.tour_crew else 0

    def get_roles(self, obj):
        return [role.role_name for role in obj.roles] if obj.roles else []

    def get_gender(self, obj):
        return obj.gender.gender_name if obj.gender else None

    def get_pronouns(self, obj):
        return obj.pronouns.pronoun_label if obj.pronouns else None
        
    
user_public_schema = UserPublicSchema()
users_public_schema = UserPublicSchema(many=True)


class UserUpdateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Users
        load_instance = False   # return dicts, not model instances
        partial = True          # allow partial updates
        include_fk = False      # user should not update raw FK values unless explicitly allowed
        include_relationships = False
        
    # Editable fields
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    phone = ma.auto_field()
    city = ma.auto_field()
    state_province = ma.auto_field()
    country = ma.auto_field()
    continent = ma.auto_field()
    bio = ma.auto_field()
    profile_picture_url = ma.auto_field()

    # Foreign key updates (allowed)
    gender_id = ma.auto_field()
    pronouns_id = ma.auto_field()

    # Password is load-only
    password = fields.String(load_only=True)
    
user_update_schema = UserUpdateSchema()
users_update_schema = UserUpdateSchema(many=True)