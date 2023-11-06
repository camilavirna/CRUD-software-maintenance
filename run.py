# from server.routes import server
# server.run()
from app.server import Server

server = Server()
server.start()
