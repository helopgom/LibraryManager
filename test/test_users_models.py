from models.UsersModel import UsersModel


def test_create_user():
    users_model = UsersModel()
    success, message = users_model.create_user(
        dni="12345678",
        user_name="Juan",
        user_lastname="Pérez",
        mail="juan.perez@example.com",
        phone="123456789"
    )
    assert success, f"Error: {message}"
    print("Create user test passed!")


def test_delete_user():
    users_model = UsersModel()
    # Primero, crea un usuario para obtener un ID válido
    success, message = users_model.create_user(
        dni="87654321",
        user_name="Ana",
        user_lastname="García",
        mail="ana.garcia@example.com",
        phone="987654321"
    )
    assert success, f"Error: {message}"

    # Busca el ID del usuario creado
    users = users_model.search_user(dni="87654321")
    if not users:
        print("No se encontró el usuario para eliminar.")
        return

    user_id = users[0]['user_id']

    success, message = users_model.delete_user(user_id)
    assert success, f"Error: {message}"
    print("Delete user test passed!")


def test_update_user():
    users_model = UsersModel()
    # Primero, crea un usuario para obtener un ID válido
    success, message = users_model.create_user(
        dni="11223344",
        user_name="Carlos",
        user_lastname="Hernández",
        mail="carlos.hernandez@example.com",
        phone="111223344"
    )
    assert success, f"Error: {message}"

    # Busca el ID del usuario creado
    users = users_model.search_user(dni="11223344")
    if not users:
        print("No se encontró el usuario para actualizar.")
        return

    user_id = users[0]['user_id']

    success, message = users_model.update_user(
        user_id=user_id,
        dni="11223344",
        user_name="Carlos",
        user_lastname="Hernández",
        mail="carlos.hernandez@updated.com",
        phone="111223344"
    )
    assert success, f"Error: {message}"
    print("Update user test passed!")


def test_search_user():
    users_model = UsersModel()
    # Primero, crea un usuario para asegurarnos de que hay algo que buscar
    success, message = users_model.create_user(
        dni="55667788",
        user_name="Laura",
        user_lastname="Martínez",
        mail="laura.martinez@example.com",
        phone="222334455"
    )
    assert success, f"Error: {message}"

    users = users_model.search_user(dni="55667788")
    assert users, "No se encontraron usuarios con el DNI proporcionado."
    print("Search user test passed!")


if __name__ == "__main__":
    test_create_user()
    test_update_user()
    test_delete_user()
    test_search_user()