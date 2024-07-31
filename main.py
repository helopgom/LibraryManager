from config import DbConnection
from models.BooksModel import BooksModel
from config.DbConnection import Connection



# Instancia del modelo BooksModel
book = BooksModel()

# Datos del libro de ejemplo
data = {
    'title': "Aire",
    'author': "Maria Suarez",
    'isbn': "5698569",
    'year_edition': "2023-12-12",
    'category_id_categories': 2
}

# Función para crear un libro
def create_book():
    add_book_id = book.create(book.table_name, data)
    if add_book_id:
        print(f'Libro insertado con éxito.')
    else:
        print(f'Error al insertar el libro.')



# Función para actualizar los datos de un libro (requiere criterios y datos a actualizar)
def update_book_data(criteria, new_data):
    update_book_result = book.update(book.table_name, new_data, criteria)
    if update_book_result:
        print(f'Libro actualizado con éxito.')
    else:
        print(f'Error al actualizar el libro.')


# Función para eliminar un libro (requiere un criterio)
def delete_book(criteria):
    delete_book_result = book.delete(book.table_name, criteria)
    if delete_book_result:
        print(f'Libro eliminado con éxito.')
    else:
        print(f'Error al eliminar el libro.')


# Función para consultar o filtrar la información

def query_books(criteria=None):

    if criteria:
        criteria_str = ", ".join([f"{key} = {value}" for key, value in criteria.items()])
        print(f"\nConsultando libros con criterio/s: '{criteria_str}'")
    else:
        print("\nConsultando todos los libros.")

    query_books_result = book.read(book.table_name, criteria)
    if query_books_result:
        for row in query_books_result:
            print(row)
    else:
        print("No se encontraron resultados.")



# Ejemplo de uso
if __name__ == "__main__":
    # #Crear libro
    # create_book()

    # # Criterios para actualizar un libro y los nuevos datos
    # update_criteria = {'title': 'Fuego'}
    # new_data = {'title': 'Fuego', 'author': 'Juan Moreno', 'year_edition': '2013-01-01'}
    # update_book_data(update_criteria, new_data)

    # # Eliminar un libro con un criterio específico (por ejemplo, por ISBN)
    # delete_criteria = {'title': 'Tierra'}
    # delete_book(delete_criteria)

    # # Consultar todos los libros
    # print("Consultando todos los libros:")
    # query_books()


