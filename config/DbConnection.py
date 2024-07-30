import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

# Cargar las variables de entorno del .env
load_dotenv()


class Connection:
    _instance = None  # permite crear una única Instancia (patron singleton)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    # Constructor
    def __init__(self):
        #  aseguramos que se inicialice una vez
        if self._connection is None:
            try:
                self._connection = psycopg2.connect(host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'),
                                                    user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
                                                    database=os.getenv('DB_NAME'))
                self._connection.autocommit = True
                print("Conexión establecida con Postgresql")
            except Error as e:
                print(f'Error con la conexión a Postgresql: {e}')
                self._connection = None

    def get_connection(self):
        return self._connection

    def execute_query(self, query, params=None):
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Error as e:
            print(f'ocurrio un error en la ejecución de la query: {e}')
        finally:
            cursor.close()

    def update_query(self, query, params=None):
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount
        except Error as e:
            print(f'ocurrio un error en la ejecución de la query: {e}')
        finally:
            cursor.close()

    def close_connection(self):
        if self._connection:
            self._connection.close()
            print('conexión cerrada')
            self._connection = None