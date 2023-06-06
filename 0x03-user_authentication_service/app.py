#!/usr/bin/env python3
""" a flaskk app module """
from flask import Flask, jsonify, request, abort
from flask_cors import (CORS, cross_origin)
from auth import Auth


AUTH = Auth()
app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.route('/', strict_slashes=False)
def home():
    """GET /
        RETURNS A JSONIFY RESPONSE
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        usr = AUTH.register_user(email, password)
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400

    if usr is not None:
        return jsonify({"email": email, "message": "user created"})
    else:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or password is None:
        abort(401)
        
    if AUTH.valid_login(email, password):
        session = AUTH.create_session(email)
        if session:
            json = jsonify({"email": email, "message": "logged in"})
            json.set_cookie('session_id', session)
            return json
        else:
            abort(401)
    else:
        abort(401)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
