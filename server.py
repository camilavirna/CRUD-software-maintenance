from flask import Flask, render_template, make_response, request, redirect, abort
from db import *
import os

class Server():

	def __init__(self):

		self.app = Flask(__name__ , static_url_path='/')
		self.app.template_folder = 'templates/'
		self.app.static_folder = 'templates/'

	def start(self):

		@self.app.route('/dashboard')

		def dashboard():

			try:

				sessionID = request.cookies.get('sessionID')
				dados = cookies.verify(sessionID)

				if dados == None:

					response = make_response(redirect('/login?erro=4'))
					response.set_cookie('sessionID', '', expires=0)
					return response
					
				else:

					return render_template('dashboard.html', nome=dados[0][2])

			except Exception as erro_na_validacao_do_cookie:

				print(erro_na_validacao_do_cookie)

				return abort(400)

		@self.app.route('/')
		
		def redirectloginpage():
			
			return redirect('/login')

		@self.app.route('/login')

		def login():

			sessionID = request.cookies.get('sessionID')

			if sessionID == 'None':

				response = make_response(redirect('/login?erro=4'))
				response.set_cookie('sessionID', '', expires=0)
				return response

			elif sessionID == None:

				return render_template('login.html')

			else:

				return redirect('/dashboard')
				

		@self.app.route('/login/validate')

		def validatelogin():

			user = request.args['email'].lower()
			passw = request.args['pswd']
			mensagem_de_validacao , cookie = loginverify(user, passw)

			if mensagem_de_validacao == 'sucesso':

				response = make_response(redirect('/dashboard'))
				response.set_cookie('sessionID', cookie)
				return response

			elif mensagem_de_validacao == 'não cadastrado':

				return redirect('/login?erro=0')

			else:

				return redirect('/login?erro=1')



		@self.app.route('/signup/validate')

		def signup():

			user = request.args['user']
			email = request.args['email'].lower()
			passw = request.args['pswd']

			mensagem_de_validacao = register(user,email, passw)

			if mensagem_de_validacao == 'sucesso':

				return redirect('/login?erro=3')

			elif mensagem_de_validacao == 'existe':

				return redirect('/login?erro=2')

		@self.app.route('/logout')

		def logout():

			sessionID = request.cookies.get('sessionID')

			if sessionID == None:

				return redirect('/login?erro=4')

			else:

				deleted = cookies.delete(sessionID)

				if deleted: 

					response = make_response(redirect('/login'))
					response.set_cookie('sessionID', '', expires=0)
					return response


				else:

					return redirect('/login?erro=4')


		self.app.run(debug=False, port=5000)


server = Server()
server.start()