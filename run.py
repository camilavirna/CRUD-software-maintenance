import threading
from waitress import serve
from app.routes import Aplication
from server.routes import server

thread = threading.Thread(target=serve,args=(server,),kwargs={"host":"0.0.0.0","port":5001})
thread.start()

server = Aplication("http://127.0.0.1:5001/")
server.start()
