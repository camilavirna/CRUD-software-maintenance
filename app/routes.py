import os

import requests
from flask import Flask, abort, make_response, redirect, render_template, request


class App:
    def __init__(self, url_base):
        self.app = Flask(__name__, static_url_path="/")
        self.app.template_folder = "templates/"
        self.app.static_folder = "static/"
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
                    user = response["user"]
                    return render_template("dashboard.html",user=user)

            except Exception as e:
                print(e)

                return abort(400)

        @self.app.route("/",methods=["GET","POST"])
        def redirectloginpage():
            return redirect("/login")

        @self.app.route("/login")
        def login():
            return render_template("login.html")

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
            return make_response(redirect("/login"))        
        
        @self.app.route("/update",methods=["GET","POST"])
        def update():
            body = {
                "email": request.form.get('email'),
                "password": request.form.get('password'),
                "nome": request.form.get('nome'),
                "telefone": request.form.get('telefone'),
                "id":request.form.get('id'),
            }
            requests.put(self.url_base + f"user/{body['id']}", json=body)
            return redirect(f"/dashboard/{body['id']}")
        
        self.app.run(
            debug=True, port=int(os.environ.get("PORT", 5000)), host="0.0.0.0"
        )