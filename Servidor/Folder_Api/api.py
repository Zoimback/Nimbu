"""Scrip - Api Para la insercion de datos proveniente de los sensores de los ESP.
   Los datos se almacenaran en la Base de Datos Mysql, BBDD Temp.

    Hecho por: Alejandro Rodríguez González.
"""

from flask import Flask, request, jsonify


# Crear una instancia de la aplicación Flask
app = Flask(__name__)


@app.route('/check')
def checker():
    """Check de la conexion al servidor y la version de la Api

    Returns:
        int: 1 --> Version local de la Api 
    """
    return 1





# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
