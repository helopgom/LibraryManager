import psycopg2
from psycopg2 import errors
from config.DbConnection import Connection
from models.BaseModel import BaseModel
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class GeneralModel(BaseModel):
    def __init__(self):
        super().__init__()
        try:
            self.connection = Connection().get_connection()
            if self.connection is None:
                raise ConnectionError("No se pudo establecer la conexión con la base de datos.")
        except Exception as e:
            logger.error(f"Error al intentar conectar a la base de datos: {e}")
            self.connection = None

    def _execute_query(self, query, params, fetch=False):
        if not self.connection:
            logger.error("No hay conexión a la base de datos.")
            return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                self.connection.commit()
                return cursor.rowcount
        except (psycopg2.Error, errors.DatabaseError) as e:
            self.connection.rollback()
            logger.error(f"Error en la consulta: {e}")
            return None

    def create(self, table, data):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        return self._execute_query(query, list(data.values()))

    def read(self, table, criteria=None):
        query = f"SELECT * FROM {table}"
        params = []
        if criteria:
            query += " WHERE " + ' AND '.join([f"{key}=%s" for key in criteria.keys()])
            params = list(criteria.values())
        return self._execute_query(query, params, fetch=True)

    def update(self, table, data, criteria):
        set_clause = ', '.join([f"{key}=%s" for key in data.keys()])
        where_clause = ' AND '.join([f"{key}=%s" for key in criteria.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        return self._execute_query(query, list(data.values()) + list(criteria.values()))

    def delete(self, table, criteria):
        where_clause = ' AND '.join([f"{key}=%s" for key in criteria.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        return self._execute_query(query, list(criteria.values()))
