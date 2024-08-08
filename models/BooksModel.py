import psycopg2
from models.GeneralModel import GeneralModel
import logging


class BooksModel(GeneralModel):
    def __init__(self):
        super().__init__()
        self.table_name = 'books'

    # Función para crear un libro
    def create_book(self, data):
        isbn = data.get('isbn')

        try:
            if self.check_duplicate_book(isbn):
                logging.info(f'El libro con el ISBN {isbn} ya existe.')
            else:
                add_book = self.create(self.table_name, data)
                if add_book:
                    logging.info(f'Libro insertado con éxito.')
                else:
                    logging.error(f'Error al insertar el libro.')
        except psycopg2.Error as e:
            logging.error(f"Error al crear el libro: {e}")

    # Función para comprobar si un libro ya existe
    def check_duplicate_book(self, isbn):
        try:
            results = self.read(self.table_name, {'isbn': isbn})
            return bool(results)
        except psycopg2.Error as e:
            logging.error(f"Error al crear el libro: {e}")

    # Función para actualizar los datos de un libro (requiere criterios y datos a actualizar)
    def update_book_data(self, criteria, new_data):
        try:
            update_book_result = self.update(self.table_name, new_data, criteria)
            if update_book_result:
                logging.info(f'Libro actualizado con éxito.')
            else:
                logging.error(f'Error al actualizar el libro.')
        except psycopg2.Error as e:
            logging.error(f"Error al actualizar los datos: {e}")

    # Función para eliminar un libro (requiere un criterio)
    def delete_book(self, criteria):
        try:
            delete_book_result = self.delete(self.table_name, criteria)
            if delete_book_result:
                logging.info(f'Libro eliminado con éxito.')
            else:
                logging.error(f'Error al eliminar el libro.')
        except psycopg2.Error as e:
            logging.error(f"Error al eliminar el libro: {e}")

    # Función para consultar o filtrar la información
    def query_books(self, criteria=None):
        try:
            if criteria:
                criteria_str = ", ".join([f"{key} = {value}" for key, value in criteria.items()])
                logging.info(f"\nConsultando libros con criterio/s: '{criteria_str}'")
            else:
                logging.info("\nConsultando todos los libros.")

            query_books_result = self.read(self.table_name, criteria)
            if query_books_result:
                for row in query_books_result:
                    print(row)
            else:
                logging.info("No se encontraron resultados.")
        except psycopg2.Error as e:
            logging.error(f"Error en la consulta: {e}")
