import pytest
from src.controllers.UserController import UserController

"""Realización de los test del UserController @author Helena"""


@pytest.fixture
def setup_user_controller(mocker):
    """Configuración del UserController con métodos del modelUser simulado para poder hacer las comprobaciones."""

    controller = UserController()
    mocker.patch.object(controller.user_model, 'check_user')
    mocker.patch.object(controller.user_model, 'create_user')
    mocker.patch.object(controller.user_model, 'update_user')
    mocker.patch.object(controller.user_model, 'delete_user')
    mocker.patch.object(controller.user_model, 'search_users')
    return controller


def test_check_user_existing_user(setup_user_controller):
    """Given: A user with DNI 12345678 is simulated to check for existence.
        When: An attempt is made to verify if the entered user exists.
        Then: Once verified, the system should return a status code 400 with the message "Ya existe un usuario con el DNI 12345678," indicating an appropriate error message.
        """
    # Given
    setup_user_controller.user_model.check_user.return_value = "A user with DNI 12345678 already exists."
    data = {"dni": "12345678", "mail": "test@example.com"}
    # When
    response = setup_user_controller.check_user(data)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == "A user with DNI 12345678 already exists."


def test_check_user_new_user(setup_user_controller):
    """Given: A new user with DNI 87654321 does not exist in the system.
        When: A check is performed to see if the user can be created.
        Then: The system should return a status code 200 indicating that the user can be created.
    """
    # Given
    setup_user_controller.user_model.check_user.return_value = None
    data = {"dni": "87654321", "mail": "newuser@example.com"}

    # When
    response = setup_user_controller.check_user(data)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Verification successful, the user can be created.'


def test_create_user_success(setup_user_controller):
    """Given: A user passes all verification checks and is not a duplicate.
        When: An attempt is made to create the user.
        Then: The system should return a status code 201 indicating successful creation.
        """

    # Given
    setup_user_controller.user_model.check_user.return_value = None
    setup_user_controller.user_model.create_user.return_value = True
    data = {"dni": "87654321", "mail": "newuser@example.com"}

    # When
    response = setup_user_controller.create_user(data)

    # Then
    assert response['status_code'] == 201
    assert response['response'] == 'User created successfully.'


def test_create_user_existing_user(setup_user_controller):
    """ Given: A user with DNI 12345678 already exists.
        When: An attempt is made to create a user with the same DNI.
        Then: The system should return a status code 400 with an error message.
    """
    # Given
    setup_user_controller.user_model.check_user.return_value = "A user with DNI 12345678 already exists."
    data = {"dni": "12345678", "mail": "test@example.com"}

    # When
    response = setup_user_controller.create_user(data)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == "A user with DNI 12345678 already exists."


def test_update_user_success(setup_user_controller):
    """Given: A user with ID 1 exists, and new data is provided for updating.
        When: An attempt is made to update the user's information.
        Then: The system should return a status code 200 indicating that the update was successful.
    """
    # Given
    user_id = 1
    data = {"mail": "updateduser@example.com"}
    setup_user_controller.user_model.update_user.return_value = True

    # When
    response = setup_user_controller.update_user(user_id, data)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'User updated successfully.'


def test_update_user_failure(setup_user_controller):
    """Given: A user with ID 1 exists, and there is an email address that causes a conflict.
        When: An attempt is made to update the user's information with conflicting data.
        Then: The system should return a status code 400 indicating that the update failed.
        """
    # Given
    user_id = 1
    data = {"mail": "conflictingemail@example.com"}
    setup_user_controller.user_model.update_user.return_value = None

    # When
    response = setup_user_controller.update_user(user_id, data)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == 'Could not update the user.'


def test_delete_user_success(setup_user_controller):
    """Given: A user with ID 1 exists and can be deleted.
        When: An attempt is made to delete the user.
        Then: The system should return a status code 200 indicating that the deletion was successful.
    """
    # Given
    user_id = 1
    setup_user_controller.user_model.delete_user.return_value = True

    # When
    response = setup_user_controller.delete_user(user_id)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'The user was successfully deleted.'


def test_delete_user_failure(setup_user_controller):
    """Given: A user with ID 1 exists and cannot be deleted.
        When: An attempt is made to delete the user.
        Then: The system should return a status code 400 indicating that the deletion failed.
    """
    # Given
    user_id = 1
    setup_user_controller.user_model.delete_user.return_value = None

    # When
    response = setup_user_controller.delete_user(user_id)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == 'Could not delete the user.'


def test_search_users_found(setup_user_controller):
    """Given: A search criterion that matches an existing user is simulated.
        When: The search is performed using the selected criterion.
        Then: The system should return a status code 200 with the search results.
    """
    # Given
    criteria = {"name": "Test User"}
    expected_result = [{"user_id": 1, "name": "Test User", "mail": "test@example.com"}]
    setup_user_controller.user_model.search_users.return_value = expected_result

    # When
    response = setup_user_controller.search_users(criteria)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == expected_result


def test_search_users_not_found(setup_user_controller):
    """Given: A search criterion is simulated that does not match any user in the database.
        When: A search is performed using this non-matching criterion.
        Then: The system should return a status code 404 with a message indicating that no users were found.
    """
    # Given
    criteria = {"name": "Nonexistent User"}
    setup_user_controller.user_model.search_users.return_value = []

    # When
    response = setup_user_controller.search_users(criteria)

    # Then
    assert response['status_code'] == 404
    assert response['response'] == 'No users found with those criteria.'
