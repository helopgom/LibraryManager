from config.DbConnection import Connection
from models.BooksModel import BooksModel

def main():
    try:
        # Inicializar la conexión a la base de datos
        conn_instance = Connection()
        print("Conexión a la base de datos inicializada.")

        # Crear una instancia del modelo BooksModel
        books_model = BooksModel()

        # Datos para el nuevo libro
        title = "El señor"
        author = "tolkien"
        isbn = "97200565"
        year_edition = "1920-04-10"  # Fecha en formato YYYY-MM-DD
        category_id_categories = 2  # Asegúrate de que este ID de categoría exista en la tabla 'categories'

        # Insertar el nuevo libro
        print("Intentando insertar el libro...")
        books_model.create(title, author, isbn, year_edition, category_id_categories)

    except Exception as e:
        print(f"Error en el proceso principal: {e}")
    finally:
        # Cerrar la conexión al finalizar
        conn_instance.close_connection()

if __name__ == "__main__":
    main()

