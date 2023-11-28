import os

import requests
from flask import Flask, abort, make_response, redirect, render_template, request



class System:
    def __init__(self, url_base):
        self.system = Flask(__name__, static_url_path="/")
        self.system.template_folder = "templates/"
        self.system.static_folder = "static/"
        self.url_base = url_base

    def loginverify(self, email, senha):
        params = {'user/email': email}
        response = requests.get(self.url_base, params=params)
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
        self.setup_routes()

    def setup_routes(self):
        self.aplication.route("/dashboard/<id>", methods=["GET"])(self.dashboard_route)
        self.aplication.route("/admin", methods=["GET"])(self.admin_route)
        self.aplication.route("/", methods=["GET", "POST"])(self.redirect_login_page_route)
        self.aplication.route("/login")(self.login_route)
        self.aplication.route("/login/validate/", methods=["GET"])(self.validate_login_route)
        self.aplication.route("/signup/validate")(self.signup_route)

    def dashboard_route(self, id):
        try:
            response = self.get_user_data_by_id(id)
            
            if response.status_code != 200:
                return make_response(redirect("/login?erro=4"))
                
            user = response.json()["user"]
            return render_template("dashboard.html", user=user)
        
        except Exception as e:
            return self.handle_error(e)

    def admin_route(self):
        try:
            response = requests.get(self.url_base + "user")
            
            if response.status_code != 200:
                return make_response(redirect("/login?erro=4"))
                
            users = response.json()["user"]
            return render_template("admin.html", users=users)
        
        except Exception as e:
            return self.handle_error(e)

    def redirect_login_page_route(self):
        return redirect("/login")

    def login_route(self):
        return render_template("login.html")

    def validate_login_route(self):
        email, passw = request.args.get("email", "").lower(), request.args.get("pswd", "")
        mensagem_de_validacao, id_session = self.loginverify(email, passw)

        if mensagem_de_validacao == "sucesso":
            return self.handle_successful_login(email, id_session)
        elif mensagem_de_validacao == "não cadastrado":
            return redirect("/login?erro=0")
        else:
            return redirect("/login?erro=1")

    def signup_route(self):
        user, email, passw = request.args["user"], request.args["email"].lower(), request.args["pswd"]
        mensagem_de_validacao = self.register(user, email, passw)

        if mensagem_de_validacao == "sucesso":
            return redirect("/login?erro=3")
        elif mensagem_de_validacao == "existe":
            return redirect("/login?erro=2")

    def handle_successful_login(self, email, id_session):
        if email == "admin@gmail.com":
            return make_response(redirect("/admin"))
        return make_response(redirect(f"/dashboard/{id_session}"))

    def get_user_data_by_id(self, user_id):
        return requests.get(self.url_base + f"user/id={user_id}")

    def handle_error(self, error):
        # Log the error or handle it as appropriate for your application
        print(error)
        return abort(400)
    
        @self.system.route("/logout")
        def logout():
            return make_response(redirect("/login"))        
        
        @self.system.route("/update",methods=["GET","POST"])
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
        
        self.system.run(
            debug=True, port=int(os.environ.get("PORT", 5000)), host="0.0.0.0"
        )