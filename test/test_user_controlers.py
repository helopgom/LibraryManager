import pytest
from unittest.mock import MagicMock
from models.UsersModel import UsersModel
import psycopg2


@pytest.fixture
def setup_users_model(mocker):
    """Fixture to setup UsersModel with mocked methods."""
    model = UsersModel()
    model._execute_query = mocker.MagicMock()
    model.create = mocker.MagicMock()
    model.update = mocker.MagicMock(return_value=True)
    model.delete = mocker.MagicMock()
    model.read = mocker.MagicMock()
    return model


def test_check_user_existing_dni(setup_users_model):
    """Test checking a user with an existing DNI."""
    # Given
    data = {"dni": "12345678X", "mail": "test@example.com"}
    setup_users_model._execute_query.return_value = [("1", "Test User", "test@example.com")]

    # When
    result = setup_users_model.check_user(data)

    # Then
    assert result == "Ya existe un usuario con el DNI 12345678X"


def test_check_user_existing_email(setup_users_model):
    """Test checking a user with an existing email."""
    # Given
    data = {"dni": "87654321X", "mail": "test@example.com"}
    setup_users_model._execute_query.side_effect = [
        [],  # No user with DNI
        [("1", "Test User", "test@example.com")]  # User with email
    ]

    # When
    result = setup_users_model.check_user(data)

    # Then
    assert result == "Ya existe un usuario con el correo test@example.com"


def test_check_user_no_existing_user(setup_users_model):
    """Test checking a user with no existing DNI or email."""
    # Given
    data = {"dni": "12345678X", "mail": "newuser@example.com"}
    setup_users_model._execute_query.side_effect = [[], []]  # No users found

    # When
    result = setup_users_model.check_user(data)

    # Then
    assert result is None


def test_create_user_success(setup_users_model):
    """Test creating a user successfully."""
    # Given
    data = {"dni": "12345678X", "mail": "newuser@example.com"}
    setup_users_model.check_user = MagicMock(return_value=None)  # No conflicts
    setup_users_model.create.return_value = True  # User creation successful

    # When
    result = setup_users_model.create_user(data)

    # Then
    assert result == True


def test_create_user_conflict(setup_users_model):
    """Test creating a user with a conflict (DNI or email already exists)."""
    # Given
    data = {"dni": "12345678X", "mail": "newuser@example.com"}
    setup_users_model.check_user = MagicMock(return_value="Ya existe un usuario con el DNI 12345678X")

    # When
    result = setup_users_model.create_user(data)

    # Then
    assert result is None


def test_update_user_success(setup_users_model):
    """Test updating a user successfully."""
    # Given
    user_id = 1
    data = {"mail": "updateduser@example.com"}
    setup_users_model.read.return_value = [("1", "Test User", "test@example.com")]
    setup_users_model.update.return_value = True

    # When
    result = setup_users_model.update_user(user_id, data)

    # Then
    assert result is True


def test_update_user_not_found(setup_users_model):
    """Test updating a user that does not exist."""
    # Given
    user_id = 1
    data = {"mail": "updateduser@example.com"}
    setup_users_model.read.return_value = []  # User not found

    # When
    result = setup_users_model.update_user(user_id, data)

    # Then
    assert result is None


def test_delete_user_success(setup_users_model):
    """Test deleting a user successfully."""
    # Given
    user_id = 1
    setup_users_model.read.return_value = [("1", "Test User", "test@example.com")]
    setup_users_model.delete.return_value = True

    # When
    result = setup_users_model.delete_user(user_id)

    # Then
    assert result == True


def test_delete_user_not_found(setup_users_model):
    """Test deleting a user that does not exist."""
    # Given
    user_id = 1
    setup_users_model.read.return_value = []  # User not found

    # When
    result = setup_users_model.delete_user(user_id)

    # Then
    assert result is None


def test_search_users_success(setup_users_model):
    """Test searching for users successfully."""
    # Given
    criteria = {"mail": "test@example.com"}
    setup_users_model.read.return_value = [("1", "Test User", "test@example.com")]

    # When
    result = setup_users_model.search_users(criteria)

    # Then
    assert result == [("1", "Test User", "test@example.com")]


def test_search_users_error(setup_users_model):
    """Test error handling during search."""
    # Given
    criteria = {"mail": "test@example.com"}
    setup_users_model.read.side_effect = psycopg2.Error("Database error")

    # When
    result = setup_users_model.search_users(criteria)

    # Then
    assert result is None
