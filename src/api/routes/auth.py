from flask import Blueprint, jsonify, request
from src.models import User
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, create_refresh_token
)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    ---
    parameters:
      - in: body
        name: user
        description: The user to login
        schema:
            type: object
            required:
                - username
                - password
            properties:
                username:
                    type: string
                password:
                    type: string

    responses:
        200:
            description: Successful login with JWT tokens
            schema:
                type: object
                properties:
                    access_token:
                        type: string
                    refresh_token:
                        type: string
        401:
            description: Invalid credentials
            schema:
                type: object
                properties:
                    Error:
                        type: string
    """
    user_dto = request.get_json()
    found_user = User.query.filter_by(username = user_dto['username']).first()
    if found_user and found_user.password == user_dto['password']:
        token = create_access_token(identity = str(found_user.id))
        refresh_token = create_refresh_token(identity = str(found_user.id))
        return jsonify({'access_token': token, 'refresh_token': refresh_token}), 200
    
    return jsonify({'Error': 'Invalid credentials'}), 401

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """
    Refresh JWT access token
    ---
    security:
        - Bearer: []
    parameters:
        - in: header
          name: Authorization
          type: string
          required: true
          description: Bearer refresh token

    responses:
        200:
            description: New access token
            schema:
                type: object
                properties:
                    access_token:
                        type: string

    """
    identity = get_jwt_identity()
    access_token = create_access_token(identity = identity)
    return jsonify(access_token=access_token)
