"""Script para realizar querys a traves de una pool de MySQL
"""

from os import getenv
from mysql.connector import pooling

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

def ejecutar_consulta(query):
    """_summary_

    Args:
        query (_type_): _description_
    """
    connection = connection_pool.get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()

    finally:
        connection.close()

# Ejemplos
CONSULTA_INSERT = "INSERT INTO tabla (columna1, columna2) VALUES ('valor1', 'valor2')"
ejecutar_consulta(CONSULTA_INSERT)
CONSULTA_SELECT = "SELECT * FROM tabla"
ejecutar_consulta(CONSULTA_SELECT)
