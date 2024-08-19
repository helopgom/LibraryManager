import pytest
from src.controllers.BooksController import BooksController


@pytest.fixture
def setup_books_controller(mocker):
    controller = BooksController()
    mocker.patch.object(controller, 'check_duplicate_book')
    mocker.patch.object(controller, 'create_book')
    mocker.patch.object(controller, 'update_book_data')
    mocker.patch.object(controller, 'delete_book')
    mocker.patch.object(controller, 'query_books')
    return controller


def test_create_book_success(setup_books_controller):
    """
       Given: No existing book with the given ISBN
       When: Attempting to create a new book
       Then: The book is successfully inserted
       """
    # Given
    setup_books_controller.check_duplicate_book.return_value = False
    setup_books_controller.create_book.return_value = dict(status_code=200, response='Book inserted successfully.',
                                                           result={'isbn': '12345', 'title': 'Test Book'})
    data = {'isbn': '12345', 'title': 'Test Book'}
    # When
    response = setup_books_controller.create_book(data)
    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Book inserted successfully.'
    assert response['result'] == data


def test_create_book_duplicate(setup_books_controller):
    """
       Given: A book with the given ISBN already exists
       When: Attempting to create a new book with the same ISBN
       Then: The response indicates that the book already exists
       """
    # Given
    setup_books_controller.check_duplicate_book.return_value = True
    setup_books_controller.create_book.return_value = {
        'status_code': 400,
        'response': 'The book with ISBN 12345 already exists.'
    }
    data = {'isbn': '12345', 'title': 'Test Book'}
    # When
    response = setup_books_controller.create_book(data)
    # Then
    assert response['status_code'] == 400
    assert response['response'] == 'The book with ISBN 12345 already exists.'


def test_update_book_success(setup_books_controller):
    """
       Given: The book with the given ISBN exists and can be updated
       When: Updating the book's data
       Then: The book update is successful
       """
    # Given
    setup_books_controller.update_book_data.return_value = dict(status_code=200,
                                                                response='Book updated successfully.')
    criteria = {'isbn': '12345'}
    new_data = {'title': 'Updated Test Book'}
    # When
    response = setup_books_controller.update_book_data(criteria, new_data)
    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Book updated successfully.'


def test_update_book_failure(setup_books_controller):
    """
       Given: The book with the given ISBN exists but cannot be updated
       When: Attempting to update the book's data
       Then: The book update fails
       """
    # Given
    setup_books_controller.update_book_data.return_value = dict(status_code=500,
                                                                response='Error updating the book.')
    criteria = {'isbn': '12345'}
    new_data = {'title': 'Updated Test Book'}
    # When
    response = setup_books_controller.update_book_data(criteria, new_data)
    # Then
    assert response['status_code'] == 500
    assert response['response'] == 'Error updating the book.'


def test_delete_book_success(setup_books_controller):
    """
       Given: The book with the given ISBN exists and can be deleted
       When: Attempting to delete the book
       Then: The book is successfully deleted
       """
    # Given
    setup_books_controller.delete_book.return_value = dict(status_code=200, response='Book deleted successfully.')
    criteria = {'isbn': '12345'}
    # When
    response = setup_books_controller.delete_book(criteria)
    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Book deleted successfully.'


def test_delete_book_failure(setup_books_controller):
    """
       Given: The book with the given ISBN exists but cannot be deleted
       When: Attempting to delete the book
       Then: The book deletion fails
       """
    # Given
    setup_books_controller.delete_book.return_value = dict(status_code=500, response='Error deleting the book.')
    criteria = {'isbn': '12345'}
    # When
    response = setup_books_controller.delete_book(criteria)
    # Then
    assert response['status_code'] == 500
    assert response['response'] == 'Error deleting the book.'


def test_query_books_found(setup_books_controller):
    """
       Given: Books that match the query criteria exist
       When: Querying books with the criteria
       Then: The query returns results successfully
       """
    # Given
    expected_result = [{'isbn': '12345', 'title': 'Test Book'}]
    setup_books_controller.query_books.return_value = dict(status_code=200, response='Query successful.',
                                                           result=expected_result)
    criteria = {'isbn': '12345'}
    # When
    response = setup_books_controller.query_books(criteria)
    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Query successful.'
    assert response['result'] == expected_result


def test_query_books_not_found(setup_books_controller):
    """
        Given: No books match the query criteria
        When: Querying books with the criteria
        Then: The query returns no results
        """
    # Given
    setup_books_controller.query_books.return_value = dict(status_code=404, response='No results found.')
    criteria = {'isbn': 'nonexistent_isbn'}
    # When
    response = setup_books_controller.query_books(criteria)
    # Then
    assert response['status_code'] == 404
    assert response['response'] == 'No results found.'


def test_check_duplicate_book_existing(setup_books_controller):
    """
       Given: A book with the given ISBN exists
       When: Checking if the book is a duplicate
       Then: The response indicates the book is a duplicate
       """
    # Given
    setup_books_controller.check_duplicate_book.return_value = True
    isbn = '12345'
    # When
    is_duplicate = setup_books_controller.check_duplicate_book(isbn)
    # Then
    assert is_duplicate is True


def test_check_duplicate_book_not_existing(setup_books_controller):
    """
      Given: No book with the given ISBN exists
      When: Checking if the book is a duplicate
      Then: The response indicates the book is not a duplicate
      """
    # Given
    setup_books_controller.check_duplicate_book.return_value = False
    isbn = 'nonexistent_isbn'
    # When
    is_duplicate = setup_books_controller.check_duplicate_book(isbn)
    # Then
    assert is_duplicate is False
