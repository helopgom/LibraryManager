import pytest
from unittest.mock import MagicMock
from models.UsersModel import UsersModel


@pytest.fixture
def users_model():
    """Fixture para inicializar el modelo de usuarios con una base de datos simulada"""
    model = UsersModel()
    model.db = MagicMock()
    return model


def test_create_user_success(users_model):
    """Test para la creación exitosa de un usuario"""
    # Simula que no existen usuarios con el mismo DNI o correo
    users_model.db.execute_query.return_value = []
    # Simula la inserción exitosa del nuevo usuario
    users_model.db.execute_query.return_value = None

    # Llama a la función create_user y verifica que se crea el usuario correctamente
    success, error = users_model.create_user('123456789', 'Raquel', 'Casado', 'raquel@gmail.com', '123456789')
    assert success is True
    assert error is None


def test_create_user_duplicate(users_model):
    """Test para verificar la creación duplicada de un usuario"""
    # Simula que ya existe un usuario con el mismo DNI o correo
    users_model.db.execute_query.return_value = [{'user_id': 1}]

    # Llama a la función create_user y verifica que se detecta el usuario duplicado
    success, error = users_model.create_user('123456789', 'Raquel', 'Casado', 'raquel@gmail.com', '123456789')
    assert success is False
    assert error == "Usuario ya existe con el mismo DNI o correo electrónico."



def test_update_user_success(users_model):
    """Test para la actualización exitosa de un usuario"""
    # Simula un resultado exitoso de la actualización
    users_model.db.execute_query.return_value = None

    # Llama a la función update_user y verifica que se actualiza el usuario correctamente
    success, error = users_model.update_user(1, '123456789', 'Raquel', 'Casado', 'raquel@gmail.com', '123456789')
    assert success is True
    assert error is None


def test_delete_user_success(users_model):
    """Test para la eliminación exitosa de un usuario"""
    # Simula un resultado exitoso de la eliminación
    users_model.db.execute_query.return_value = None

    # Llama a la función delete_user y verifica que se elimina el usuario correctamente
    success, error = users_model.delete_user(1)
    assert success is True
    assert error is None
