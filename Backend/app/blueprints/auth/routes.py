from . import auth_bp
from .schemas import signup_schema, login_schema
from app.blueprints.users.schemas import UserSchema, user_schema
from app.utility.auth import encode_token, require_system_role, token_required
from flask import request, jsonify
from app.models import Users, UserRoles
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, limiter


# ============================================================
# 1. USER SIGNUP
# ============================================================
@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        # Validate input
        user_data = signup_schema.load(request.json)

        # Check duplicate email BEFORE creating anything
        email = user_data.get("email")
        if Users.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already registered'}), 400

        # Hash password
        hashed_password = generate_password_hash(user_data['password'])

        # Create user
        new_user = Users(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=hashed_password,
            phone=user_data.get('phone'),
            city=user_data.get('city'),
            state_province=user_data.get('state_province'),
            country=user_data.get('country'),
            continent=user_data.get('continent'),
            bio=user_data.get('bio'),
            dob=user_data.get('dob'),
            gender_id=user_data.get('gender_id'),
            pronouns_id=user_data.get('pronouns_id')
        )
        db.session.add(new_user)
        db.session.flush()  # ensures new_user.id is available

        # Assign roles
        role_ids = user_data.get('roles', [])
        for role_id in role_ids:
            db.session.add(UserRoles(user_id=new_user.id, role_id=role_id))

        # Commit everything
        db.session.commit()

        return user_schema.jsonify(new_user), 201

    except ValidationError as err:
        db.session.rollback()
        return jsonify(err.messages), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============================================================
# 2. USER LOGIN
# ============================================================

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        login_data = login_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    user = Users.query.filter_by(email=login_data['email']).first()
    if not user or not check_password_hash(user.password, login_data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    # No role restriction — both "user" and "admin" can log in
    token = encode_token(user.id, user.system_role)

    return jsonify({'token': token}), 200
