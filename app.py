from flask import Flask

# Crea l'istanza dell'app
app = Flask(__name__)

# Definisce la rotta principale (/)
@app.route('/')
def hello_world():
    # Ritorna la stringa "hello world"
    return 'hello world'

# Avvia l'app se il file viene eseguito direttamente
if __name__ == '__main__':
    # Esegui su host '0.0.0.0' per essere accessibile
    # dall'esterno del container.
    # La porta 5000 è quella predefinita di Flask.
    app.run(host='0.0.0.0', port=5000)