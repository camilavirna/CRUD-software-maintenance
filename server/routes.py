import logging
import os

from flask import request

from server import create_server
from server.models import User
from server.utils import generate_response
from flask_cors import CORS

from . import db

logging.basicConfig(level=logging.INFO)
server = create_server(os.getenv("FLASK_CONFIG"))
CORS(server)

@server.route("/user", methods=["GET"])
def get_users():
    users = User.query.all()  # Consulta todos os usuários da tabela User
    users_json = [user.serialize() for user in users]
    logging.info("GET: ALL")
    return generate_response(200, "user", users_json, "ok")


@server.route("/user/id=<id>", methods=["GET"])
def get_user_id(id):
    user = User.query.get(id)  # Consulta o usuário da tabela
    if user:
        logging.info("GET: %s", user)
        return generate_response(200, "user", user.serialize(), "ok")
    return generate_response(404, "user", {}, "user not found")


@server.route("/user/email=<email>", methods=["GET"])
def get_user_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        logging.info("GET: %s", user)
        return generate_response(200, "user", user.serialize(), "ok")
    return generate_response(404, "user", {}, "user not found")


@server.route("/user", methods=["POST"])
def create_user():
    try:
        user = User(
            id=request.json.get("id"),
            email=request.json.get("email"),
            password=request.json.get("password"),
            nome=request.json.get("nome"),
            telefone=request.json.get("telefone"),
        )
        db.session.add(user)
        db.session.commit()
        logging.info("POST: %s", user)
        return generate_response(201, "user", user.serialize(), "successfully created")
    except Exception as e:
        print(e)
        return generate_response(400, "user", {}, "error creating user")


@server.route("/user/<id>", methods=["PUT"])
def update_user(id):
    user_object = User.query.get(id)
    body = request.get_json()
    if user_object and body:
        try:
            for field in ["id", "email", "password", "nome", "telefone"]:
                if field in body:
                    setattr(user_object, field, body[field])

            db.session.add(user_object)
            db.session.commit()
            logging.info("PUT: %s", user_object)
            return generate_response(
                200, "user", user_object.serialize(), "successfully updated"
            )
        except Exception as e:
            print(e)
            return generate_response(400, "user", {}, "error update user")

    return generate_response(404, "user", {}, "user not found")


@server.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    user_object = User.query.get(id)
    if user_object:
        try:
            db.session.delete(user_object)
            db.session.commit()
            logging.info("DELETE: %s", user_object)
            return generate_response(
                200, "user", user_object.serialize(), "successfully deleted"
            )
        except Exception as e:
            print(e)
            return generate_response(400, "user", {}, "error delete user")
    return generate_response(404, "user", {}, "user not found")
