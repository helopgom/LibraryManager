import pytest
from src.controllers.UserController import UserController


@pytest.fixture
def setup_user_controller(mocker):
    """Fixture to setup UserController with mocked UsersModel."""
    controller = UserController()
    mocker.patch.object(controller.user_model, 'check_user')
    mocker.patch.object(controller.user_model, 'create_user')
    mocker.patch.object(controller.user_model, 'update_user')
    mocker.patch.object(controller.user_model, 'delete_user')
    mocker.patch.object(controller.user_model, 'search_users')
    return controller


def test_check_user_existing_user(setup_user_controller):
    """Test when user already exists in the system."""
    # Given
    setup_user_controller.user_model.check_user.return_value = "Ya existe un usuario con el DNI 12345678"
    data = {"dni": "12345678", "mail": "test@example.com"}

    # When
    response = setup_user_controller.check_user(data)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == "Ya existe un usuario con el DNI 12345678"


def test_check_user_new_user(setup_user_controller):
    """Test when user does not exist and can be created."""
    # Given
    setup_user_controller.user_model.check_user.return_value = None
    data = {"dni": "87654321", "mail": "newuser@example.com"}

    # When
    response = setup_user_controller.check_user(data)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Verificación exitosa, el usuario puede ser creado'


def test_create_user_success(setup_user_controller):
    """Test successful user creation."""
    # Given
    setup_user_controller.user_model.check_user.return_value = None
    setup_user_controller.user_model.create_user.return_value = True
    data = {"dni": "87654321", "mail": "newuser@example.com"}

    # When
    response = setup_user_controller.create_user(data)

    # Then
    assert response['status_code'] == 201
    assert response['response'] == 'Usuario creado con éxito'


def test_create_user_existing_user(setup_user_controller):
    """Test attempting to create a user that already exists."""
    # Given
    setup_user_controller.user_model.check_user.return_value = "Ya existe un usuario con el DNI 12345678"
    data = {"dni": "12345678", "mail": "test@example.com"}

    # When
    response = setup_user_controller.create_user(data)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == "Ya existe un usuario con el DNI 12345678"


def test_update_user_success(setup_user_controller):
    """Test successful user update."""
    # Given
    user_id = 1
    data = {"mail": "updateduser@example.com"}
    setup_user_controller.user_model.update_user.return_value = True

    # When
    response = setup_user_controller.update_user(user_id, data)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Usuario actualizado con éxito'


def test_update_user_failure(setup_user_controller):
    """Test user update failure due to conflict."""
    # Given
    user_id = 1
    data = {"mail": "conflictingemail@example.com"}
    setup_user_controller.user_model.update_user.return_value = None

    # When
    response = setup_user_controller.update_user(user_id, data)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == 'No se pudo actualizar el usuario'


def test_delete_user_success(setup_user_controller):
    """Test successful user deletion."""
    # Given
    user_id = 1
    setup_user_controller.user_model.delete_user.return_value = True

    # When
    response = setup_user_controller.delete_user(user_id)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'El usuario fue eliminado de manera exitosa'


def test_delete_user_failure(setup_user_controller):
    """Test user deletion failure."""
    # Given
    user_id = 1
    setup_user_controller.user_model.delete_user.return_value = None

    # When
    response = setup_user_controller.delete_user(user_id)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == 'No se pudo eliminar el usuario'


def test_search_users_found(setup_user_controller):
    """Test searching users with results found."""
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
    """Test searching users with no results found."""
    # Given
    criteria = {"name": "Nonexistent User"}
    setup_user_controller.user_model.search_users.return_value = []

    # When
    response = setup_user_controller.search_users(criteria)

    # Then
    assert response['status_code'] == 404
    assert response['response'] == 'No se encontraron usuarios con esos criterios'
