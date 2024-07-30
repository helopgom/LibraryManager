from config.DbConnection import Connection
from models.BaseModel import BaseModel


class BooksModel(BaseModel):

    def __init__(self):
        super().__init__()
        self.connection = Connection().get_connection()
        if self.connection is None:
            raise Exception("No se pudo establecer una conexión a la base de datos.")

    def create(self, title, author, isbn, year_edition, category_id_categories):
        if not self.connection:
            print("No se pudo establecer una conexión a la base de datos.")
            return

        try:
            cursor = self.connection.cursor()
            print(f"Insertando libro: {title}, {author}, {isbn}, {year_edition}, {category_id_categories}")
            query = """
                INSERT INTO books (title, author, isbn, year_edition, category_id_categories)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (title, author, isbn, year_edition, category_id_categories))
            self.connection.commit()
            print("Libro insertado correctamente.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error creando libro: {e}")
        finally:
            if cursor:
                cursor.close()

    def read(self, book_id):
        if not self.connection:
            print("No se pudo establecer una conexión a la base de datos.")
            return None

        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM books WHERE book_id = %s"
            cursor.execute(query, (book_id,))
            result = cursor.fetchone()
            print(f"Libro leído: {result}")
            return result
        except Exception as e:
            print(f"Error leyendo libro: {e}")
        finally:
            if cursor:
                cursor.close()

    def update(self, book_id, title=None, author=None, isbn=None, year_edition=None, category_id_categories=None):
        if not self.connection:
            print("No se pudo establecer una conexión a la base de datos.")
            return

        try:
            cursor = self.connection.cursor()
            set_clause = []
            params = []

            if title:
                set_clause.append("title = %s")
                params.append(title)
            if author:
                set_clause.append("author = %s")
                params.append(author)
            if isbn:
                set_clause.append("isbn = %s")
                params.append(isbn)
            if year_edition:
                set_clause.append("year_edition = %s")
                params.append(year_edition)
            if category_id_categories:
                set_clause.append("category_id_categories = %s")
                params.append(category_id_categories)

            if not set_clause:
                print("No se proporcionaron campos para actualizar.")
                return

            params.append(book_id)
            query = f"UPDATE books SET {', '.join(set_clause)} WHERE book_id = %s"
            cursor.execute(query, tuple(params))
            self.connection.commit()
            print("Libro actualizado correctamente.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error actualizando libro: {e}")
        finally:
            if cursor:
                cursor.close()

    def delete(self, book_id):
        if not self.connection:
            print("No se pudo establecer una conexión a la base de datos.")
            return

        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM books WHERE book_id = %s"
            cursor.execute(query, (book_id,))
            self.connection.commit()
            print("Libro eliminado correctamente.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error eliminando libro: {e}")
        finally:
            if cursor:
                cursor.close()
