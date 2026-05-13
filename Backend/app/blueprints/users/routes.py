from app.blueprints.users import users_bp
from app.blueprints.users.schemas import UserSchema, UserPublicSchema, UserUpdateSchema
from app.utility.auth import token_required, require_system_role
from flask import request, jsonify
from app.models import Users
from app.extensions import db, limiter
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin

#________________USER PROFILE ROUTES__________________
            # - All users have the same access. 
            # - Admin users can access all profiles, while regular users can only access their own profile.
            # - Admin have an admin able to approve/reject tours, manage users, and oversee the overall system. Regular users can only access their own profile and perform actions related to their account.
            
# ============================================================
# 1. GET CURRENT USER PROFILE
# ============================================================
# USED FOR: Retrieving the profile information of the currently authenticated user
@users_bp.route('/me', methods=['GET'])
@token_required
def get_current_user_profile(current_user):
    
    user_schema = UserSchema()
    return jsonify(user_schema.dump(current_user)), 200


# ============================================================
# 2. UPDATE CURRENT USER PROFILE
# ============================================================
# USED FOR: Allowing the currently authenticated user to update their profile information
@users_bp.route('/me', methods=['PUT'])
@token_required
def update_current_user_profile(current_user):
    data = request.get_json()
    
    # Validate incoming data
    try:
        user_update_schema = UserUpdateSchema(partial=True)  # Allow partial updates
        validated_data = user_update_schema.load(data) # This will raise a ValidationError if the data is invalid
        
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    
    # Update user fields
    for key, value in validated_data.items():
        if key == 'password':
            value = generate_password_hash(value)  # Hash the password before saving
        setattr(current_user, key, value)
    
    db.session.commit()
    
    user_schema = UserSchema()
    return jsonify(user_schema.dump(current_user)), 200

# ============================================================
# 3. DELETE CURRENT USER PROFILE
# ============================================================
# USED FOR: Allowing the currently authenticated user to delete their profile
@users_bp.route('/me', methods=['DELETE'])
@token_required
def delete_current_user_profile(current_user):
    
    #Fetch the user
    delete_user = Users.query.get(current_user.id)
    if not delete_user:
        return jsonify({"error": "User not found."}), 404
    if delete_user.id != current_user.id:
        return jsonify({"error": "Unauthorized to delete this profile."}), 403
    
    db.session.delete(delete_user)
    db.session.commit()
    return jsonify({"message": "User profile deleted successfully."}), 200

# history of his jobs should remain in the system, but marked as "deleted user" or something similar. This way we can maintain the integrity of the data and the history of interactions, while respecting the user's choice to delete their profile.

