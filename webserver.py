from flask import Flask #keep alive
from threading import Thread #keep alive


#webserver
app = Flask('')
@app.route('/')
def home():
    return "Your Bot Is Ready"

def run():
    app.run(host="0.0.0.0", port=8000)
    
def keep_alive():
    server = Thread(target=run)
    server.start()