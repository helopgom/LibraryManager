import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os
import logging

load_dotenv()


class Connection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def __init__(self):
        if self._connection is None:
            try:
                self._connection = psycopg2.connect(host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'),
                                                    user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
                                                    database=os.getenv('DB_NAME'))
                self._connection.autocommit = True
                logging.info("Connection established with PostgreSQL.")
            except Error as e:
                logging.error(f'Error with the connection to PostgreSQL: {e}')
                self._connection = None

    def get_connection(self):
        return self._connection

    def execute_query(self, query, params=None):
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Error as e:
            logging.error(f'An error occurred during the execution of the query: {e}')
        finally:
            cursor.close()

    def update_query(self, query, params=None):
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount
        except Error as e:
            logging.info(f'An error occurred during the execution of the query: {e}')
        finally:
            cursor.close()

    def close_connection(self):
        if self._connection:
            self._connection.close()
            logging.info('Connection closed.')
            self._connection = None
