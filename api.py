"""Scrip - Api Para la insercion de datos proveniente de los sensores de los ESP.
   Los datos se almacenaran en la Base de Datos Mysql, BBDD Temp.

    Hecho por: Alejandro Rodríguez González.
"""

from flask import Flask, request
import conexiones_mysql


# Crear una instancia de la aplicación Flask
app = Flask(__name__)


@app.route('/check')
def checker():
    """Check de la conexion al servidor y la version de la Api

    Returns:
        int: 1 --> Version local de la Api 
    """
    return 1

@app.route('/insert', methods=['POST'])
def insercion():
    """Método para recivir datos  a traves de un json del ESP32 y enviar a una BBDD. 

    Returns:
        JSON: GOOD / BAD (strings)
    """
    try:
        nombre_esp=request.json['esp']
        dato_temperatura=request.json["temp"]
        query = f"INSERT INTO Datos (ESP, TEMP ) VALUES ('{nombre_esp}' ,'{dato_temperatura}')"
        conexiones_mysql.ejecutar_consulta(query)
        return "GOOD"
    except Exception as e:
        print(str(e))
        return "BAD"



# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
