
import pytest
from src.controllers import UserController

@pytest.fixture
def user_controller(mocker):
    mock_users_model = mocker.patch('src.controllers.UserController.UsersModel')
    mock_instance = mock_users_model.return_value
    return UserController(), mock_instance

@pytest.fixture
def usuario_no_existe(mocker):
    mock_controller = mocker.MagicMock(UserController)
    mock_controller.create_user.return_value = (True, 'Usuario creado con éxito')  # Simula la respuesta esperada
    mock_controller.update_user.return_value = (True, 'Usuario actualizado con éxito')
    mock_controller.delete_user.return_value = (True, 'Usuario eliminado con éxito')
    mock_controller.get_user.return_value = []  # Simula que no hay usuarios
    return mock_controller

@pytest.fixture
def usuario_existe(mocker):
    mock_controller = mocker.MagicMock(UserController)
    mock_controller.create_user.return_value = (False, 'El usuario ya existe')  # Simula que el usuario ya existe
    mock_controller.update_user.return_value = (False, 'Error al actualizar el usuario')
    mock_controller.delete_user.return_value = (False, 'Error al eliminar el usuario')
    mock_controller.get_user.return_value = [
        {'dni': '12345678', 'name': 'Juan', 'lastname': 'Pérez', 'email': 'juan.perez@example.com', 'phone': '1234567890'}
    ]
    return mock_controller

def test_create_user_exitoso(usuario_no_existe):
    """
    Scenario: Registro exitoso de un nuevo usuario
      Given que no existe un usuario con DNI "12345678"
      When intento registrar un usuario con DNI "12345678", nombre "Juan", apellido "Perez", email "juan.perez@example.com", y teléfono "1234567890"
      Then el usuario es creado exitosamente y recibo un código de estado 200
    """
    controller = usuario_no_existe
    result = controller.create_user('12345678', 'Juan', 'Perez', 'juan.perez@example.com', '1234567890')

    # Verificaciones
    assert result == (True, 'Usuario creado con éxito')

def test_create_user_ya_existente(usuario_existe):
    """
    Scenario: Intento de registro de un usuario ya existente
      Given que existe un usuario con DNI "12345678"
      When intento registrar un usuario con DNI "12345678", nombre "Juan", apellido "Perez", email "juan.perez@example.com", y teléfono "1234567890"
      Then recibo un error indicando que el usuario ya existe y un código de estado 400
    """
    controller = usuario_existe
    result = controller.create_user('12345678', 'Juan', 'Perez', 'juan.perez@example.com', '1234567890')

    # Verificaciones
    assert result == (False, 'El usuario ya existe')

def test_update_user_exitoso(usuario_existe):
    """
    Scenario: Actualización exitosa de la información del usuario
      Given que existe un usuario con DNI "12345678"
      When intento actualizar la información del usuario con DNI "12345678" con nombre "Juanito", apellido "Pérez", email "juanito.perez@example.com", y teléfono "0987654321"
      Then la información del usuario es actualizada exitosamente y recibo un código de estado 200
    """
    controller = usuario_existe
    result = controller.update_user('12345678', '12345678', 'Juanito', 'Pérez', 'juanito.perez@example.com', '0987654321')

    # Verificaciones
    assert result == (True, 'Usuario actualizado con éxito')
def test_update_user_no_existente(usuario_no_existe):
    """
    Scenario: Intento de actualización de información de un usuario que no existe
      Given que no existe un usuario con DNI "12345678"
      When intento actualizar la información del usuario con DNI "12345678" con nombre "Juanito", apellido "Pérez", email "juanito.perez@example.com", y teléfono "0987654321"
      Then recibo un error indicando que el usuario no existe y un código de estado 400
    """
    controller = usuario_no_existe
    result = controller.update_user('12345678', '12345678', 'Juanito', 'Pérez', 'juanito.perez@example.com', '0987654321')

    # Verificaciones
    assert result == (False, 'Error al actualizar el usuario')

def test_delete_user_exitoso(usuario_existe):
    """
    Scenario: Eliminación exitosa de un usuario
      Given que existe un usuario con DNI "12345678"
      When intento eliminar al usuario con DNI "12345678"
      Then el usuario es eliminado exitosamente y recibo un código de estado 200
    """
    controller = usuario_existe
    result = controller.delete_user('12345678')

    # Verificaciones
    assert result == (True, 'Usuario eliminado con éxito')
def test_delete_user_no_existente(usuario_no_existe):
    """
    Scenario: Intento de eliminación de un usuario que no existe
      Given que no existe un usuario con DNI "12345678"
      When intento eliminar al usuario con DNI "12345678"
      Then recibo un error indicando que el usuario no existe y un código de estado 400
    """
    controller = usuario_no_existe
    result = controller.delete_user('12345678')

    # Verificaciones
    assert result == (False, 'Error al eliminar el usuario')
def test_search_users_encontrado(usuario_existe):
    """
    Scenario: Búsqueda exitosa de un usuario
      Given que existe un usuario con DNI "12345678"
      When busco al usuario con DNI "12345678"
      Then recibo los datos del usuario y un código de estado 200
    """
    controller = usuario_existe
    result = controller.get_user(dni='12345678')

    # Verificaciones
    assert len(result) == 1
    assert result[0]['dni'] == '12345678'
    assert result[0]['name'] == 'Juan'
    assert result[0]['lastname'] == 'Pérez'
    assert result[0]['email'] == 'juan.perez@example.com'
    assert result[0]['phone'] == '1234567890'

def test_search_users_no_encontrado(usuario_no_existe):
    """
    Scenario: Búsqueda de un usuario que no existe
      Given que no existe un usuario con DNI "12345678"
      When busco al usuario con DNI "12345678"
      Then recibo un mensaje indicando que no se encontraron usuarios y un código de estado 404
    """
    controller = usuario_no_existe
    result = controller.get_user(dni='12345678')

    # Verificaciones
    assert len(result) == 0


