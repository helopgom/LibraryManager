import pytest
from src.controllers.BooksController import BooksController


@pytest.fixture
def setup_books_controller(mocker):
    """Configuración del BooksController con métodos del modelo BooksModel simulados."""
    controller = BooksController()
    mocker.patch.object(controller.book_model, 'create')
    mocker.patch.object(controller.book_model, 'read')
    mocker.patch.object(controller.book_model, 'update')
    mocker.patch.object(controller.book_model, 'delete')
    return controller


def test_create_book_success(setup_books_controller):
    """Simula la creación exitosa de un libro que no existe en la base de datos."""
    # Given
    setup_books_controller.book_model.read.return_value = []
    setup_books_controller.book_model.create.return_value = True
    data = {'isbn': '12345', 'title': 'Test Book'}

    # When
    response = setup_books_controller.create_book(data)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Libro insertado con éxito.'
    assert response['result'] == data


def test_create_book_duplicate(setup_books_controller):
    """Simula un intento de creación de un libro con un ISBN que ya existe."""
    # Given
    setup_books_controller.book_model.read.return_value = [{'isbn': '12345', 'title': 'Existing Book'}]
    data = {'isbn': '12345', 'title': 'Test Book'}

    # When
    response = setup_books_controller.create_book(data)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == 'El libro con el ISBN 12345 ya existe.'


def test_update_book_success(setup_books_controller):
    """Simula la actualización exitosa de un libro existente."""
    # Given
    setup_books_controller.book_model.update.return_value = True
    criteria = {'isbn': '12345'}
    new_data = {'title': 'Updated Test Book'}

    # When
    response = setup_books_controller.update_book_data(criteria, new_data)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Libro actualizado con éxito.'


def test_update_book_failure(setup_books_controller):
    """Simula un fallo en la actualización de un libro."""
    # Given
    setup_books_controller.book_model.update.return_value = False
    criteria = {'isbn': '12345'}
    new_data = {'title': 'Updated Test Book'}

    # When
    response = setup_books_controller.update_book_data(criteria, new_data)

    # Then
    assert response['status_code'] == 500
    assert response['response'] == 'Error al actualizar el libro.'


def test_delete_book_success(setup_books_controller):
    """Simula la eliminación exitosa de un libro."""
    # Given
    setup_books_controller.book_model.delete.return_value = True
    criteria = {'isbn': '12345'}

    # When
    response = setup_books_controller.delete_book(criteria)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Libro eliminado con éxito.'


def test_delete_book_failure(setup_books_controller):
    """Simula un fallo en la eliminación de un libro."""
    # Given
    setup_books_controller.book_model.delete.return_value = False
    criteria = {'isbn': '12345'}

    # When
    response = setup_books_controller.delete_book(criteria)

    # Then
    assert response['status_code'] == 500
    assert response['response'] == 'Error al eliminar el libro.'


def test_query_books_found(setup_books_controller):
    """Simula una consulta que devuelve resultados."""
    # Given
    criteria = {'isbn': '12345'}
    expected_result = [{'isbn': '12345', 'title': 'Test Book'}]
    setup_books_controller.book_model.read.return_value = expected_result

    # When
    response = setup_books_controller.query_books(criteria)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Consulta exitosa.'
    assert response['result'] == expected_result


def test_query_books_not_found(setup_books_controller):
    """Simula una consulta que no devuelve ningún resultado."""
    # Given
    criteria = {'isbn': 'nonexistent_isbn'}
    setup_books_controller.book_model.read.return_value = []

    # When
    response = setup_books_controller.query_books(criteria)

    # Then
    assert response['status_code'] == 404
    assert response['response'] == 'No se encontraron resultados.'


def test_check_duplicate_book_existing(setup_books_controller):
    """Simula la verificación de un libro duplicado que ya existe en la base de datos."""
    # Given
    setup_books_controller.book_model.read.return_value = [{'isbn': '12345', 'title': 'Existing Book'}]
    isbn = '12345'

    # When
    is_duplicate = setup_books_controller.check_duplicate_book(isbn)

    # Then
    assert is_duplicate is True


def test_check_duplicate_book_not_existing(setup_books_controller):
    """Simula la verificación de un libro que no existe en la base de datos."""
    # Given
    setup_books_controller.book_model.read.return_value = []
    isbn = 'nonexistent_isbn'

    # When
    is_duplicate = setup_books_controller.check_duplicate_book(isbn)

    # Then
    assert is_duplicate is False
