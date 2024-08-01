from models.BooksModel import BooksModel
import psycopg2


class BooksController:
    def __init__(self):
        self.book_model = BooksModel()

    def create_book(self, data):
        isbn = data.get('isbn')
        try:
            if self.check_duplicate_book(isbn):
                return dict(status_code=400, response=f'El libro con el ISBN {isbn} ya existe.')
            else:
                add_book = self.book_model.create(self.book_model.table_name, data)
                if add_book:
                    return dict(status_code=200, response='Libro insertado con éxito.', result=data)
                else:
                    return dict(status_code=500, response='Error al insertar el libro.')
        except psycopg2.Error as e:
            return dict(status_code=500, response=f"Error al crear el libro: {e}")

    def check_duplicate_book(self, isbn):
        try:
            results = self.book_model.read(self.book_model.table_name, {'isbn': isbn})
            return bool(results)
        except psycopg2.Error as e:
            return dict(status_code=500, response=f"Error al verificar el libro duplicado: {e}")

    def update_book_data(self, criteria, new_data):
        try:
            update_book_result = self.book_model.update(self.book_model.table_name, new_data, criteria)
            if update_book_result:
                return dict(status_code=200, response='Libro actualizado con éxito.')
            else:
                return dict(status_code=500, response='Error al actualizar el libro.')
        except psycopg2.Error as e:
            return dict(status_code=500, response=f"Error al actualizar los datos: {e}")

    def delete_book(self, criteria):
        try:
            delete_book_result = self.book_model.delete(self.book_model.table_name, criteria)
            if delete_book_result:
                return dict(status_code=200, response='Libro eliminado con éxito.')
            else:
                return dict(status_code=500, response='Error al eliminar el libro.')
        except psycopg2.Error as e:
            return dict(status_code=500, response=f"Error al eliminar el libro: {e}")

    def query_books(self, criteria=None):
        try:
            query_books_result = self.book_model.read(self.book_model.table_name, criteria)
            if query_books_result:
                return dict(status_code=200, response='Consulta exitosa.', result=query_books_result)
            else:
                return dict(status_code=404, response='No se encontraron resultados.')
        except psycopg2.Error as e:
            return dict(status_code=500, response=f"Error en la consulta: {e}")
