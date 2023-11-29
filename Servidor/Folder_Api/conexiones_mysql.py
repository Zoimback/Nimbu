"""Script para realizar querys a traves de una pool de MySQL
"""

from os import getenv
from mysql.connector import pooling
import json
from datetime import date

# Configuración de la conexión a la base de datos MySQL
db_params = {
    'host': getenv('host'),
    'user': getenv('user'),
    'password': getenv('password'),
    'database': 'Temp',
}

# Crear un pool de conexiones sin límite superior
connection_pool = pooling.MySQLConnectionPool(pool_name="pool",
                                              pool_size=32,
                                              **db_params)

def ejecutar_consulta(query, is_select):
    """_summary_

    Args:
        query (string): Query para hacer a la base de datos
        is_select (bool): Mira si la query en una insercion o una selección de datos
    """
    connection = connection_pool.get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query)

        if is_select:  # Si es una consulta SELECT
            results = cursor.fetchall()
            #print(results)
            rows = []
            for row in results:
                row_data = {
                    'ESP': str(row[0]),
                    'TEMPERATURA': str(row[1]),
                    'FECHA': str(row[2].strftime("%Y-%m-%d"))
                }
                rows.append(row_data)

            # Devolver los resultados como JSON
            return json.dumps(rows)
        else:  # Si es una consulta de inserción, actualización o eliminación
            connection.commit()
            return json.dumps({"status": "OK", "message": "Operación realizada correctamente."})

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        return json.dumps({"status": "Error", "message": f"Error en la operación: {str(e)}"})

    finally:
        cursor.close()
        connection.close()


# Ejemplos
#CONSULTA_INSERT = "INSERT INTO tabla (columna1, columna2) VALUES ('valor1', 'valor2')"
#ejecutar_consulta(CONSULTA_INSERT)
#CONSULTA_SELECT = "SELECT ESP, TEMP, DATE FROM Datos WHERE DATE >= '2023-10-23'  AND DATE <= '2023-10-24' AND 'Sensor-2' = ESP;"
#ejecutar_consulta(CONSULTA_SELECT, is_select=True)
