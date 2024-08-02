from config.DbConnection import Connection
from models.BooksModel import BooksModel
from models.CategoriesModel import CategoriesModel

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

    # Crear una instancia de CategoriesModel
    categories_model = CategoriesModel()

    # Datos para una nueva categoría
    category_data = {
        'category_id': 1,  # Cambia el ID para probar con un nuevo valor
        'category_name': 'Ficción'
    }

    # **1. Crear una nueva categoría si no existe**
    print("\nVerificando y creando una categoría...")
    if categories_model.check_category(category_id=category_data['category_id']):
        print("La categoría ya existe.")
    else:
        result = categories_model.create_category(
            category_data['category_id'],
            category_data['category_name']
        )
        if result:
            print("Categoría creada con éxito.")
        else:
            print("No se pudo crear la categoría.")

    # **2. Actualizar una categoría existente**
    update_data = {
        'category_id': 5,
        'category_name': 'Thriller'
    }
    print("\nActualizando categoría...")
    update_result = categories_model.update(
        update_data['category_id'],
        update_data['category_name']
    )
    if update_result:
        print("Categoría actualizada con éxito.")
    else:
        print("No se pudo actualizar la categoría.")

    # **3. Buscar categorías existentes**
    search_criteria = {
        'category_name': 'Ficción'
    }
    print("\nBuscando categorías...")
    search_results = categories_model.search_and_filter(
        category_name=search_criteria['category_name']
    )
    if search_results:
        print("Categorías encontradas:")
        for category in search_results:
            print(category)
    else:
        print("No se encontraron categorías con esos criterios.")


