import json

from flask import Response


def generate_response(status, name_content, content, message=False):
    body = {}
    body[name_content] = content
    if message:
        body["message"] = message
    return Response(
        json.dumps(body, default=str), status=status, mimetype="aplication/json"
    )
