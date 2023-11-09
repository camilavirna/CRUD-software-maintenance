import threading

from app.routes import App
from server.routes import server

thread = threading.Thread(target=server.run)
thread.start()

server = App("http://127.0.0.1:5000/")
server.start()
