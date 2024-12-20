#!/usr/bin/env python3
"task 7"
from flask import request, jsonify, make_response
from models.user import User
from api.v1.views import app_views
from api.v1.app import auth
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Login a user and create a session ID if credentials are valid.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.id)
    response = make_response(user.to_json())
    session_name = os.getenv("SESSION_NAME", "_my_session_id")
    response.set_cookie(session_name, session_id)
    return response
