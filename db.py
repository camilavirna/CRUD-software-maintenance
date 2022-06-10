import sqlite3
import random
import string

def random_generator(size=40, chars=string.ascii_uppercase + string.digits):

	return ''.join(random.choice(chars) for _ in range(size))

def connectdb():

	conn = sqlite3.connect('sqlite/database.db')
	cursor = conn.cursor()
	cursor.execute(""" CREATE TABLE IF NOT EXISTS usuarios(email TEXT NOT NULL, password TEXT NOT NULL , nome TEXT NOT null, sessionID TEXT)""")
	conn.commit()
	return conn, cursor 


def loginverify(usuario, senha):

	conn, cursor = connectdb()
	dados = cursor.execute(""" SELECT password from usuarios where email = (?)""",(usuario,)).fetchall()

	if dados == []:

		return 'não cadastrado' , None

	elif dados[0][0] == senha:

		dados = cursor.execute(""" SELECT * from usuarios where email = (?)""",(usuario,)).fetchall()
		return 'sucesso', cookies.create(usuario,senha)

	else:

		return 'incorreta', None

def register(nome,email,passw):

	
	conn, cursor = connectdb()
	dados = cursor.execute(""" SELECT email FROM usuarios WHERE email = (?)""",(email,)).fetchall()
	
	if dados == []:

		cursor.execute(""" INSERT INTO usuarios(email,password,nome, sessionID) VALUES(?,?,?,?) """, (email,passw,nome,'None',))
		conn.commit()
		return 'sucesso'
	
	else:

		return 'existe'


class cookies:

	def verify(sessionID):

		conn, cursor = connectdb()
		dados = cursor.execute(""" SELECT * FROM usuarios WHERE sessionID = (?) """ , (sessionID,)).fetchall()
		
		if dados == []:

			return None

		elif sessionID == 'None':

			return None

		else:

			return dados

	def create(email, senha):

		conn , cursor = connectdb()
		cookie = random_generator()
		cursor.execute(""" UPDATE usuarios SET sessionID = (?) WHERE email = (?) AND password = (?) """, (cookie,email,senha,))
		conn.commit()
		return cookie

	def delete(sessionID):

		conn , cursor = connectdb()
		dados = cursor.execute(""" SELECT * FROM usuarios WHERE sessionID = (?) """ , (sessionID,)).fetchall()
		
		if not dados == [] and sessionID != 'None':

			cursor.execute(""" UPDATE usuarios SET sessionID = (?) WHERE sessionID = (?)""", ('None',sessionID,))
			conn.commit()
			return True

		else:

			return False