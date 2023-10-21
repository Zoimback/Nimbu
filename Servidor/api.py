from flask import Flask

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Definir una ruta para la página principal
@app.route('/')
def hello_world():
    return 'Hola, mundo!'

# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')