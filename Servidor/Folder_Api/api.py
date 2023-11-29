"""Scrip - Api Para la insercion de datos proveniente de los sensores de los ESP.
   Los datos se almacenaran en la Base de Datos Mysql, BBDD Temp.

    Hecho por: Alejandro Rodríguez González.
"""

from datetime import date, timedelta
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify
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
        tiempo1 --> Fecha mayor
        tiempo2 --> Fecha menor

    Returns:
        JSON: GOOD / BAD (strings)
    """
    tiempo1=request.json['tiempo1']
    tiempo2=request.json["tiempo2"]
    nombresensor=request.json["sensor"]

    if tiempo1 == tiempo2 :
        tiempo2 = tiempo2 + timedelta(days=1)
    elif tiempo1 < tiempo2:
        return "BAD, Date error" 

    #fechahoy= date.today().strftime("%Y-%m-%d")
    query = f" SELECT ESP, TEMP, DATE FROM Datos WHERE DATE >= '{tiempo1}' AND DATE <= '{tiempo2}'  AND '{nombresensor}' = ESP;"
    resultados=conexiones_mysql.ejecutar_consulta(query)

    # Convertir los resultados a una lista de diccionarios para jsonify
    lista_resultados = []
    for resultado in resultados:
        diccionario_resultado = {
            'ESP': resultado[0],
            'TEMPERATURA': resultado[1],
            'FECHA': resultado[2].strftime("%Y-%m-%d")  # Formatear la fecha si es necesario
        }
        lista_resultados.append(diccionario_resultado)

    # Retornar los datos como JSON
    return jsonify({"status": "GOOD", "data": lista_resultados})



# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
