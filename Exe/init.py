"""
Script nucleo del exe
"""
import requests, json

url ='http://192.168.1.20:5000'

def obtenerdatos():
    select_api = requests.get(f'{url}/obtain', json={"tiempo1": "2023-11-28","tiempo2":"2023-11-30","sensor":"Sensor-2"})
    print(select_api.text)
obtenerdatos()



