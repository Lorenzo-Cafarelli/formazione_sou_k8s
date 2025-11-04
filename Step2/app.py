# app.py
from flask import Flask

# Crea l'istanza dell'applicazione Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    # Restituisce la stringa "hello world"
    return 'hello world'

if __name__ == '__main__':
    # Esegue l'applicazione sulla porta 8080 (come specificato nel Dockerfile)
    # L'host 0.0.0.0 rende l'applicazione accessibile dall'esterno del container
    app.run(debug=True, host='0.0.0.0', port=8080)