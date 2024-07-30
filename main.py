# main.py
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
        title = "El Gran Gatsby"
        author = "F. Scott Fitzgerald"
        isbn = "9780565"
        year_edition = "1925-04-10"
        category_id_categories = 1

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
