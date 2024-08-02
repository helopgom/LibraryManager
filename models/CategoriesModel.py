import psycopg2
from psycopg2 import errors
from models.GeneralModel import GeneralModel

class CategoriesModel(GeneralModel):
    def __init__(self):
        super().__init__()

    def create_category(self, category_id, category_name):
        query = "INSERT INTO categories (category_id, category_name) VALUES (%s, %s)"
        params = (category_id, category_name)
        return self._execute_query(query, params)

    def search_and_filter(self, category_id=None, category_name=None):
        query = "SELECT * FROM categories"
        params = []
        filters = []

        if category_id is not None:
            filters.append("category_id = %s")
            params.append(category_id)
        if category_name is not None:
            filters.append("category_name ILIKE %s")
            params.append(f"%{category_name}%")

        if filters:
            query += " WHERE " + " AND ".join(filters)

        return self._execute_query(query, params, fetch=True)

    def check_category(self, category_id=None, category_name=None):
        query = "SELECT EXISTS(SELECT 1 FROM categories WHERE"
        params = []

        if category_id is not None:
            query += " category_id = %s"
            params.append(category_id)
        if category_name is not None:
            if len(params) > 0:
                query += " AND"
            query += " category_name ILIKE %s"
            params.append(f"%{category_name}%")

        query += ")"

        result = self._execute_query(query, params, fetch=True)
        return result[0][0] if result else False

    def update(self, category_id, new_name):
        query = "UPDATE categories SET category_name = %s WHERE category_id = %s"
        params = (new_name, category_id)
        return self._execute_query(query, params)

    def delete(self, category_id):
        query = "DELETE FROM categories WHERE category_id = %s"
        params = (category_id,)
        return self._execute_query(query, params)

    def _execute_query(self, query, params, fetch=False):
        if not self.connection:
            print("No hay conexión a la base de datos.")
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
            print(f"Error en la consulta: {e}")
            return None
