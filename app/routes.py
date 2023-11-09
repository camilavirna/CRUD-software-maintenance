import os

import requests
from flask import Flask, abort, make_response, redirect, render_template, request


class App:
    def __init__(self, url_base):
        self.app = Flask(__name__, static_url_path="/")
        self.app.template_folder = "templates/"
        self.app.static_folder = "templates/"
        self.url_base = url_base

    def loginverify(self, email, senha):
        response = requests.get(self.url_base + f"user/email={email}")
        if response.status_code != 200:
            return "não cadastrado", None
        else:
            response = response.json()
            response = response["user"]
            print(response["id"])
            if response["password"] == senha:
                return "sucesso", response["id"]
            return "incorreta", None

    def register(self, nome, email, password, telefone=0):
        response = requests.get(self.url_base + f"user/email={email}")
        if response.status_code == 404:
            body = {
                "email": email,
                "nome": nome,
                "password": password,
                "telefone": telefone,
            }
            requests.post(self.url_base + "user", json=body)
            return "sucesso"
        else:
            return "existe"

    def start(self):
        @self.app.route("/dashboard/<id>", methods=["GET"])
        def dashboard(id):
            try:
                response = requests.get(self.url_base + f"user/id={id}")
                if response.status_code != 200:
                    response = make_response(redirect("/login?erro=4"))
                    return response
                else:
                    response = response.json()
                    response = response["user"]
                    return render_template("dashboard.html", nome=response["nome"])

            except Exception as e:
                print(e)

                return abort(400)

        @self.app.route("/")
        def redirectloginpage():
            return redirect("/login")

        @self.app.route("/login")
        def login():
            sessionID = request.cookies.get("sessionID")

            if sessionID == "None":
                response = make_response(redirect("/login?erro=4"))
                response.set_cookie("sessionID", "", expires=0)
                return response

            elif sessionID == None:
                return render_template("login.html")

            else:
                return redirect("/dashboard")

        @self.app.route("/login/validate/", methods=["GET"])
        def validatelogin():
            email = request.args["email"].lower()
            passw = request.args["pswd"]
            mensagem_de_validacao, id_session = self.loginverify(email, passw)
            if mensagem_de_validacao == "sucesso":
                response = make_response(redirect(f"/dashboard/{id_session}"))
                return response

            elif mensagem_de_validacao == "não cadastrado":
                return redirect("/login?erro=0")

            else:
                return redirect("/login?erro=1")

        @self.app.route("/signup/validate")
        def signup():
            user = request.args["user"]
            email = request.args["email"].lower()
            passw = request.args["pswd"]

            mensagem_de_validacao = self.register(user, email, passw)

            if mensagem_de_validacao == "sucesso":
                return redirect("/login?erro=3")

            elif mensagem_de_validacao == "existe":
                return redirect("/login?erro=2")

        @self.app.route("/logout")
        def logout():
            sessionID = request.cookies.get("sessionID")

            if sessionID == None:
                return redirect("/login?erro=4")

            else:
                deleted = True

                if deleted:
                    response = make_response(redirect("/login"))
                    response.set_cookie("sessionID", "", expires=0)
                    return response

                else:
                    return redirect("/login?erro=4")

        self.app.run(
            debug=False, port=int(os.environ.get("PORT", 5000)), host="0.0.0.0"
        )
