"""Scrip - Api Para la insercion de datos proveniente de los sensores de los ESP.
   Los datos se almacenaran en la Base de Datos Mysql, BBDD Temp.

    Hecho por: Alejandro Rodríguez González.
"""

from datetime import date, timedelta
import xml.etree.ElementTree as ET
from flask import Flask, request
import conexiones_mysql


tree = ET.parse('/home/alex/Github/Nimbu/Servidor/Folder_Api/datos.xml')
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
        string: GOOD --> Correcto funcionamiento de la api
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


@app.route('/obtain', methods=['GET'])
def obtener():
    """Método para obtener datos que correspondan con los valores. 

    Returns:
        JSON: GOOD / BAD (strings)
    """
    tiempo1=request.json['tiempo1']
    tiempo2=request.json["tiempo2"]
    nombresensor=request.json["sensor"]

    if tiempo1 == tiempo2 :
        tiempo2 = tiempo2 + timedelta(days=1)

    #fechahoy= date.today().strftime("%Y-%m-%d")
    query = f"SELECT ESP, TEMP, DATE FROM Datos WHERE  DATE >='{tiempo1}' and DATE <= '{tiempo2} and ESP = '{nombresensor}')"
    resultado=conexiones_mysql.ejecutar_consulta(query)
    return resultado


# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
