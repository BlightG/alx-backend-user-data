#!/usr/bin/env python3
""" Module of session_authentication views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import base64
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ GET /api/v1/auth_session/login
    Return:
      - post a to log into a website
    """
    email = request.form.get('email')
    if email is None:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if password is None:
        return jsonify({"error": "password missing"}), 400

    try:
        user_l = []
        user_l = User.search({"email": email})
    except KeyError:
        return None

    if (len(user_l)) == 0:
        return jsonify({"error": "no user found for this email"}), 400

    user = user_l[0]
    if user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    print(auth)
    user_session = auth.create_session(user.id)
    json = jsonify(user.to_json())
    json.set_cookie(getenv, user_session)
    return json


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def delete_session() -> str:
    """ deletes a session """
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)

    return jsonify({}), 200
