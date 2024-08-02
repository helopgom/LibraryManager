
from config.DbConnection import Connection
from models.UsersModel import UsersModel


from models.BooksModel import BooksModel


# Instancia del modelo BooksModel
book = BooksModel()

        user_model = UsersModel()

        # Datos para un nuevo usuario
        new_user_data = {
            "dni": "13456879X",
            "user_name": "María",
            "user_lastname": "Estevez",
            "mail": "maria.estevez@example.com",
            "phone": "987654321"
        }



        # Eliminar un usuario
        print("\nIntentando eliminar un usuario...")
        result = user_model.delete_user(13)
        if result:
            print("Usuario eliminado con éxito.")
        else:
            print("No se pudo eliminar el usuario.")





    except Exception as e:
        print(f"Error en el proceso principal: {e}")
    finally:
        # Cerrar la conexión al finalizar
        conn_instance.close_connection()

# Datos del libro de ejemplo
data = {
    'title': "La  moderna",
    'author': "Francisco",
    'isbn': "9785550",
    'year_edition': "2013-01-12",
    'category_id_categories': 3
}


# Ejemplos de uso


if __name__ == "__main__":
    # Crear libro
      # book.create_book(data)

    # # Criterios para actualizar un libro y los nuevos datos
    # update_criteria = {'book_id': 22}
    # new_data = {'author': 'Rita'}
    # book.update_book_data(update_criteria, new_data)

    # # Eliminar un libro con un criterio específico (por ejemplo, por ISBN)
    # delete_criteria = {'book_id': 21}
    # book.delete_book(delete_criteria)

    # Consultar todos los libros
    book.query_books({'book_id': 23})


