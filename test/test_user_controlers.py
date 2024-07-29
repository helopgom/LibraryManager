import pytest
from unittest.mock import MagicMock
from src.controllers.UserController import UserController


@pytest.fixture
def user_controller():
    """Fixture (configuración o entorno antes de ejecutar test) para inicializar el controlador de usuarios con un
    modelo de usuario simulado"""
    controller = UserController()
    controller.user_model = MagicMock()
    return controller


def test_create_user_success(user_controller):
    """Test para la creación exitosa de un usuario desde el controlador"""
    # Simula un resultado exitoso de la creación de usuario
    user_controller.user_model.create_user.return_value = (True, None)

    # Llama al método create_user del controlador y verifica la respuesta
    response = user_controller.create_user('123456789', 'Raquel', 'Casado', 'raquel@gmail.com', '123456789')
    assert response['status_code'] == 200
    assert response['response'] == 'El usuario fue creado de manera exitosa'
    assert response['result'] == ['123456789', 'Raquel', 'Casado', 'raquel@gmail.com', '123456789']


def test_create_user_failure(user_controller):
    """Test para el fallo en la creación de un usuario desde el controlador debido a datos duplicados"""
    # Simula un fallo en la creación de usuario debido a datos duplicados
    user_controller.user_model.create_user.return_value = (
        False, 'Usuario ya existe con el mismo DNI o correo electrónico.')

    # Llama al método create_user del controlador y verifica la respuesta
    response = user_controller.create_user('123456789', 'Raquel', 'Casado', 'raquel@gmail.com', '123456789')
    assert response['status_code'] == 400
    assert response['response'] == 'Error al crear el usuario: Usuario ya existe con el mismo DNI o correo electrónico.'
    assert response['error'] == 'Usuario ya existe con el mismo DNI o correo electrónico.'


def test_delete_user_success(user_controller):
    """Test para la eliminación exitosa de un usuario desde el controlador"""
    # Simula un resultado exitoso de la eliminación de usuario
    user_controller.user_model.delete_user.return_value = (True, None)

    # Llama al método delete_user del controlador y verifica la respuesta
    response = user_controller.delete_user(1)
    assert response['status_code'] == 200
    assert response['response'] == 'El usuario fue eliminado de manera exitosa'


def test_delete_user_failure(user_controller):
    """Test para el fallo en la eliminación de un usuario desde el controlador"""
    # Simula un fallo en la eliminación de usuario
    user_controller.user_model.delete_user.return_value = (False, 'Error al eliminar el usuario')

    # Llama al método delete_user del controlador y verifica la respuesta
    response = user_controller.delete_user(1)
    assert response['status_code'] == 500
    assert response['response'] == 'Error al eliminar el usuario'
    assert response['error'] == 'Error al eliminar el usuario'


def test_update_user_success(user_controller):
    """Test para la actualización exitosa de un usuario desde el controlador"""
    # Simula un resultado exitoso de la actualización de usuario
    user_controller.user_model.update_user.return_value = (True, None)

    # Llama al método update_user del controlador y verifica la respuesta
    response = user_controller.update_user(1, '123456789', 'Raquel', 'Casado', 'raquel@gmail.com', '123456789')
    assert response['status_code'] == 200
    assert response['response'] == 'El usuario fue actualizado de manera exitosa'
    assert response['result'] == [1, '123456789', 'Raquel', 'Casado', 'raquel@gmail.com', '123456789']


def test_update_user_failure(user_controller):
    """Test para el fallo en la actualización de un usuario desde el controlador"""
    # Simula un fallo en la actualización de usuario
    user_controller.user_model.update_user.return_value = (False, 'Error al actualizar el usuario')

    # Llama al método update_user del controlador y verifica la respuesta
    response = user_controller.update_user(1, '123456789', 'Raquel', 'Casado', 'raquel@gmail.com', '123456789')
    assert response['status_code'] == 500
    assert response['response'] == 'Error al actualizar el usuario'
    assert response['error'] == 'Error al actualizar el usuario'
