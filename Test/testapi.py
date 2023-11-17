"""
Test para probar en correcto funcionamiento de la api

"""
import requests, json
url ='http://192.168.1.20:5000'

def test_check():
    """Prueba de conexion con la api.
    """
    versionapi = requests.get(f'{url}/check')
    assert versionapi.status_code == 200
    
def test_insert():
    """Test de insercion de datos
    """
    insercion_api = requests.post(f'{url}/insert', json={"esp" : "test","temp": 14})
    assert insercion_api.status_code == 200