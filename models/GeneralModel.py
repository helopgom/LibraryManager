from typing import Any, Dict, List, Optional
from config.DbConnection import Connection
import psycopg2


class GeneralModel:
    def _init_(self):
        self.connection = Connection().get_connection()

    def create(self, table: str, data: Dict[str, Any]) -> int:
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING id"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, list(data.values()))
                self.connection.commit()
                return cursor.fetchone()[0]
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error al crear en la tabla {table}: {e}")
            return 0

    def read(self, table: str, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {table}"
        params = []
        if criteria:
            query += " WHERE " + ' AND '.join([f"{key}=%s" for key in criteria.keys()])
            params = list(criteria.values())
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except psycopg2.Error as e:
            print(f"Error al leer de la tabla {table}: {e}")
            return []

    def update(self, table: str, data: Dict[str, Any], criteria: Dict[str, Any]) -> int:
        set_clause = ', '.join([f"{key}=%s" for key in data.keys()])
        where_clause = ' AND '.join([f"{key}=%s" for key in criteria.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, list(data.values()) + list(criteria.values()))
                self.connection.commit()
                return cursor.rowcount
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error al actualizar en la tabla {table}: {e}")
            return 0

    def delete(self, table: str, criteria: Dict[str, Any]) -> int:
        where_clause = ' AND '.join([f"{key}=%s" for key in criteria.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, list(criteria.values()))
                self.connection.commit()
                return cursor.rowcount
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error al eliminar de la tabla {table}: {e}")
            return 0
