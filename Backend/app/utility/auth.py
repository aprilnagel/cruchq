from datetime import datetime, timedelta, timezone
from jose import jwt
import jose 
from functools import wraps
from flask import request, jsonify
import os
from app.models import Users

SECRET_KEY = os.getenv('SECRET_KEY') or "supersecretkey"
ALGORITHM = "HS256"

#___________TOKEN ENCODING____________

def encode_token(user_id, system_role):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=24),  # Token expires in 24 hours
        "iat": datetime.now(timezone.utc),  # Issued at time
        'user_id': user_id,
        'system_role': system_role,
        'sub': str(user_id)  # Subject of the token, typically the user ID
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


#-------------TOKEN DECORATOR-------------

#___________1. Token Required Decorator____________

def token_required(f): #main function
    
    @wraps(f) #secondary function that wraps the main function, preserving its metadata
    def decorator(*args, **kwargs):
        token = None
        
        # Check if the token is provided in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Expecting "Bearer <token>" and removes "bearer" from the token string
            
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.logged_in_user_id = data['sub']  #the user ID is stored in the "sub" field of the token payload, and we attach it to the request object for later use in the route function.
            request.logged_in_user_system_role = data['system_role']  #the user's role is stored in the "system_role" field of the token payload, and we attach it to the request object for later use in the route function.
            
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        current_user = Users.query.get(request.logged_in_user_id)
        
        if not current_user:
            return jsonify({'message': 'User not found!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorator

#_______________ROLE-BASED ACCESS DECORATORS_____________________

#so for routes, we will drop in the roles when using the required decorator like @require_role("admin"), @require_role("author", "admin"), etc. if all roles are allowed, we can just use @token_required without the role requirement decorator. This way, we can have more flexible access control based on user roles.

def require_system_role(*system_roles):
    def wrapper(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if request.logged_in_user_system_role not in system_roles:
                return jsonify({'message': 'Access forbidden: insufficient permissions!'}), 403 #403 Forbidden status code for insufficient permissions
            
            return f(current_user, *args, **kwargs)
        return decorated
    return wrapper 
    