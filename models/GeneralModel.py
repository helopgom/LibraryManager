import psycopg2
from psycopg2 import errors
from config.DbConnection import Connection
from models.BaseModel import BaseModel
import logging


class GeneralModel(BaseModel):
    def __init__(self):
        super().__init__()
        try:
            self.connection = Connection().get_connection()
            if self.connection is None:
                raise ConnectionError("The connection to the database could not be established.")
        except Exception as e:
            logging.error(f"Error when trying to connect to the database: {e}")
            self.connection = None

    def _execute_query(self, query, params, fetch=False):
        if not self.connection:
            logging.error("There is no connection to the database.")
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
            logging.error(f"Error in the query: {e}")
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
