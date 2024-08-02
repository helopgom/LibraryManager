import pytest
from src.controllers.BooksController import BooksController

"""Realización de los test del BooksController"""


@pytest.fixture
def setup_books_controller(mocker):
    """Configuración del BooksController con métodos del BooksModel simulado para poder hacer las comprobaciones."""
    controller = BooksController()
    mocker.patch.object(controller.book_model, 'create_book')
    mocker.patch.object(controller.book_model, 'check_duplicate_book')
    mocker.patch.object(controller.book_model, 'update_book_data')
    mocker.patch.object(controller.book_model, 'delete_book')
    mocker.patch.object(controller.book_model, 'query_books')
    return controller


def test_create_book_success(setup_books_controller):
    """Given: Se simula un libro que pasa las verificaciones y no está duplicado.
       When: Se intenta crear el libro.
       Then: El sistema debe devolver un código de estado 200 indicando la creación exitosa.
    """
    # Given
    setup_books_controller.book_model.check_duplicate_book.return_value = False
    setup_books_controller.book_model.create_book.return_value = True
    data = {"isbn": "1234567890", "title": "Nuevo Libro", "author": "Autor Desconocido"}

    # When
    response = setup_books_controller.create_book(data)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Libro insertado con éxito.'
    assert response['result'] == data


def test_create_book_existing(setup_books_controller):
    """Given: Se simula que ya existe un libro con el ISBN 1234567890.
       When: Se intenta crear un libro con el mismo ISBN.
       Then: El sistema debe devolver un código de estado 400 con un mensaje de error.
    """
    # Given
    setup_books_controller.book_model.check_duplicate_book.return_value = True
    data = {"isbn": "1234567890", "title": "Libro Existente", "author": "Autor Existente"}

    # When
    response = setup_books_controller.create_book(data)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == 'El libro con el ISBN 1234567890 ya existe.'


def test_create_book_failure(setup_books_controller):
    """Given: Se simula un error en la base de datos durante la creación del libro.
       When: Se intenta crear el libro.
       Then: El sistema debe devolver un código de estado 500 indicando el error.
    """
    # Given
    setup_books_controller.book_model.check_duplicate_book.return_value = False
    setup_books_controller.book_model.create_book.side_effect = Exception("Database error")
    data = {"isbn": "1234567890", "title": "Nuevo Libro", "author": "Autor Desconocido"}

    # When
    response = setup_books_controller.create_book(data)

    # Then
    assert response['status_code'] == 500
    assert response['response'].startswith('Error al crear el libro')


def test_update_book_success(setup_books_controller):
    """Given: Se simula la existencia de un libro y se proporcionan nuevos datos para actualizar.
       When: Se intenta actualizar la información del libro.
       Then: El sistema debe devolver un código de estado 200 indicando que la actualización fue exitosa.
    """
    # Given
    setup_books_controller.book_model.update_book_data.return_value = True
    criteria = {"isbn": "1234567890"}
    new_data = {"title": "Título Actualizado"}

    # When
    response = setup_books_controller.update_book_data(criteria, new_data)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Libro actualizado con éxito.'


def test_update_book_failure(setup_books_controller):
    """Given: Se simula un error en la base de datos durante la actualización del libro.
       When: Se intenta actualizar el libro.
       Then: El sistema debe devolver un código de estado 500 indicando el error.
    """
    # Given
    setup_books_controller.book_model.update_book_data.side_effect = Exception("Database error")
    criteria = {"isbn": "1234567890"}
    new_data = {"title": "Título Actualizado"}

    # When
    response = setup_books_controller.update_book_data(criteria, new_data)

    # Then
    assert response['status_code'] == 500
    assert response['response'].startswith('Error al actualizar los datos')


def test_delete_book_success(setup_books_controller):
    """Given: Se simula la existencia de un libro que puede ser eliminado.
       When: Se intenta eliminar el libro.
       Then: El sistema debe devolver un código de estado 200 indicando que la eliminación fue exitosa.
    """
    # Given
    setup_books_controller.book_model.delete_book.return_value = True
    criteria = {"isbn": "1234567890"}

    # When
    response = setup_books_controller.delete_book(criteria)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Libro eliminado con éxito.'


def test_delete_book_failure(setup_books_controller):
    """Given: Se simula un error en la base de datos durante la eliminación del libro.
       When: Se intenta eliminar el libro.
       Then: El sistema debe devolver un código de estado 500 indicando el error.
    """
    # Given
    setup_books_controller.book_model.delete_book.side_effect = Exception("Database error")
    criteria = {"isbn": "1234567890"}

    # When
    response = setup_books_controller.delete_book(criteria)

    # Then
    assert response['status_code'] == 500
    assert response['response'].startswith('Error al eliminar el libro')


def test_query_books_found(setup_books_controller):
    """Given: Se simula un criterio de búsqueda que coincide con un libro existente.
       When: Se realiza la búsqueda de libros con el criterio elegido.
       Then: El sistema debe devolver un código de estado 200 con los resultados de la búsqueda realizada.
    """
    # Given
    criteria = {"author": "Autor Desconocido"}
    expected_result = [{"isbn": "1234567890", "title": "Libro Encontrado", "author": "Autor Desconocido"}]
    setup_books_controller.book_model.query_books.return_value = expected_result

    # When
    response = setup_books_controller.query_books(criteria)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Consulta exitosa.'
    assert response['result'] == expected_result


def test_query_books_not_found(setup_books_controller):
    """Given: Se simula un criterio de búsqueda que no coincide con ningún libro en la BBDD.
       When: Se realiza la búsqueda de libros con un criterio que no coincide.
       Then: El sistema debe devolver un código de estado 404 con un mensaje indicando que no se encontraron resultados.
    """
    # Given
    criteria = {"author": "Autor Inexistente"}
    setup_books_controller.book_model.query_books.return_value = []

    # When
    response = setup_books_controller.query_books(criteria)

    # Then
    assert response['status_code'] == 404
    assert response['response'] == 'No se encontraron resultados.'


def test_query_books_failure(setup_books_controller):
    """Given: Se simula un error en la base de datos durante la consulta de libros.
       When: Se intenta consultar los libros.
       Then: El sistema debe devolver un código de estado 500 indicando el error.
    """
    # Given
    setup_books_controller.book_model.query_books.side_effect = Exception("Database error")
    criteria = {"author": "Autor Desconocido"}

    # When
    response = setup_books_controller.query_books(criteria)

    # Then
    assert response['status_code'] == 500
    assert response['response'].startswith('Error en la consulta')
