"""Scrip - Api Para la insercion de datos proveniente de los sensores de los ESP.
   Los datos se almacenaran en la Base de Datos Mysql, BBDD Temp.

    Hecho por: Alejandro Rodríguez González.
"""

import xml.etree.ElementTree as ET
from flask import Flask, request
import conexiones_mysql



tree = ET.parse('datos.xml')
root = tree.getroot()


maximo_element = root.find('maximo')
minimo_element = root.find('minimo')

# Obtener los valores máximo y mínimo
maximo = float(maximo_element.text)
minimo = float(minimo_element.text)



# Crear una instancia de la aplicación Flask
app = Flask(__name__)


@app.route('/check')
def checker():
    """Check de la conexion al servidor y la version de la Api

    Returns:
        string: 1 --> Version local de la Api 
    """
    return 'GOOD'

@app.route('/insert', methods=['POST'])
def insercion():
    """Método para recivir datos  a traves de un json del ESP32 y enviar a una BBDD. 

    Returns:
        JSON: GOOD / BAD (strings)
    """
    nombre_esp=request.json['esp']
    dato_temperatura=request.json["temp"]
    if(dato_temperatura <= maximo)or(dato_temperatura >= minimo):
        query = f"INSERT INTO Datos (ESP, TEMP ) VALUES ('{nombre_esp}' ,'{dato_temperatura}')"
        conexiones_mysql.ejecutar_consulta(query)
        return "GOOD"
    return "BAD"



# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
