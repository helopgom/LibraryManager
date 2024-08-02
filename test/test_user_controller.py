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
    """Given. Se simula que existe un usuario con el DNI 12345678 para comprobar si existe.
        When: Se intenta verificar que el usuario ingresado existe.
        Then: Una vez comprobado, el sistema debe devolver 400 y en texto "Ya existe un usuario con el DNI 12345678".
                Es decir, con un mensaje de error acorde a lo que ocurre."""
    # Given
    setup_user_controller.user_model.check_user.return_value = "Ya existe un usuario con el DNI 12345678"
    data = {"dni": "12345678", "mail": "test@example.com"}
    # When
    response = setup_user_controller.check_user(data)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == "Ya existe un usuario con el DNI 12345678"


def test_check_user_new_user(setup_user_controller):
    """Given:  Se simula un nuevo usuario con el DNI 87654321 que no existe en el sistema.
        When: Se verifica si el usuario puede ser creado.
        Then: El sistema debe devolver un código de estado 200 indicando que el usuario puede ser creado.
    """
    # Given
    setup_user_controller.user_model.check_user.return_value = None
    data = {"dni": "87654321", "mail": "newuser@example.com"}

    # When
    response = setup_user_controller.check_user(data)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Verificación exitosa, el usuario puede ser creado'


def test_create_user_success(setup_user_controller):
    """Given: Se simula un usuario que pasa las verificaciones y no está duplicado.
       When: Se intenta crear el usuario.
        Then: El sistema debe devolver un código de estado 201 indicando la creación exitosa.
        """

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
    """ Given: Se simula que ya existe un usuario con el DNI 12345678.
        When: Se intenta crear el usuario con el mismo DNI.
        Then: El sistema debe devolver un código de estado 400 con un mensaje de error.
    """
    # Given
    setup_user_controller.user_model.check_user.return_value = "Ya existe un usuario con el DNI 12345678"
    data = {"dni": "12345678", "mail": "test@example.com"}

    # When
    response = setup_user_controller.create_user(data)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == "Ya existe un usuario con el DNI 12345678"


def test_update_user_success(setup_user_controller):
    """Given: Se simula la existencia de un usuario con ID 1 y se proporcionan nuevos datos para actualizar.
        When: Se intenta actualizar la información del usuario.
        Then: El sistema debe devolver un código de estado 200 indicando que la actualización fue exitosa."""
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
    """Given: Se simula la existencia de un usuario con ID 1 y un correo electrónico que genera un conflicto.
        When: Se intenta actualizar la información del usuario con datos conflictivos.
        Then: El sistema debe devolver un código de estado 400 indicando que la actualización falló."""
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
    """Given: Se simula la existencia de un usuario con ID 1 que puede ser eliminado.
        When: Se intenta eliminar el usuario.
        Then: El sistema debe devolver un código de estado 200 indicando que la eliminación fue exitosa.
    """
    # Given
    user_id = 1
    setup_user_controller.user_model.delete_user.return_value = True

    # When
    response = setup_user_controller.delete_user(user_id)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'El usuario fue eliminado de manera exitosa'


def test_delete_user_failure(setup_user_controller):
    """Given: Se simula la existencia de un usuario con ID 1 que no puede ser eliminado.
        When: Se intenta eliminar el usuario.
        Then: El sistema debe devolver un código de estado 400 indicando que la eliminación falló.
    """
    # Given
    user_id = 1
    setup_user_controller.user_model.delete_user.return_value = None

    # When
    response = setup_user_controller.delete_user(user_id)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == 'No se pudo eliminar el usuario'


def test_search_users_found(setup_user_controller):
    """Given: Se simula un criterio de búsqueda que coincide con un usuario existente.
    When: Se realiza la búsqueda de usuarios con el criterio elegido.
    Then: El sistema debe devolver un código de estado 200 con los resultados de la búsqueda realizada.
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
    """Given: Se simula un criterio de búsqueda que no coincide con ningún usuario de la BBDD.
        When: Se realiza la búsqueda de usuarios con un criterio que no coincide.
        Then: El sistema debe devolver un código de estado 404 con un mensaje indicando que no se encontraron usuarios.
    """
    # Given
    criteria = {"name": "Nonexistent User"}
    setup_user_controller.user_model.search_users.return_value = []

    # When
    response = setup_user_controller.search_users(criteria)

    # Then
    assert response['status_code'] == 404
    assert response['response'] == 'No se encontraron usuarios con esos criterios'
