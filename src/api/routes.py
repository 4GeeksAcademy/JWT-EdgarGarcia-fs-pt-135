"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import request, jsonify, Blueprint
from api.models import db, User
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.extensions import bcrypt

api = Blueprint('api', __name__)

CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if email is None:
        return jsonify({"msg": "Email is required"}), 400

    if password is None:
        return jsonify({"msg": "Password is required"}), 400

    if name is None:
        return jsonify({"msg": "Name is required"}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"msg": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        email=email,
        password=hashed_password,
        name=name,
        is_active=True
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "msg": "User created successfully",
        "user": new_user.serialize()
    }), 201


@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if email is None:
        return jsonify({"msg": "Email is required"}), 400

    if password is None:
        return jsonify({"msg": "Password is required"}), 400

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "Invalid credentials"}), 401

    is_password_valid = bcrypt.check_password_hash(
        user.password,
        password
    )

    if not is_password_valid:
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "msg": "Login successful",
        "token": token,
        "user": user.serialize()
    }), 200


@api.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if user is None:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "msg": "Profile data",
        "user": user.serialize()
    }), 200