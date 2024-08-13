from models.UsersModel import UsersModel


class UserController:
    def __init__(self):
        self.user_model = UsersModel()

    def check_user(self, data):
        """Verifica si ya existe un usuario con el mismo DNI o correo."""
        try:
            # Verifica el usuario usando el método del modelo
            verification_message = self.user_model.check_user(data)
            if verification_message:
                return dict(status_code=400, response=verification_message)
            return dict(status_code=200, response='Verification successful, the user can be created.')
        except Exception as e:
            return dict(status_code=500, response='Internal server error: ' + str(e))

    def create_user(self, data):
        """Crea un nuevo usuario después de verificar que no haya duplicados."""
        try:
            # Verificar si ya existe un usuario con el mismo DNI o correo
            verification_response = self.check_user(data)
            if verification_response['status_code'] != 200:
                return verification_response

            # Crear el nuevo usuario si la verificación fue exitosa
            result = self.user_model.create_user(data)
            if result:
                return dict(status_code=201, response='User created successfully.')
            else:
                return dict(status_code=400, response='Could not create the user.')
        except Exception as e:
            return dict(status_code=500, response='Internal server error: ' + str(e))

    def update_user(self, user_id, data):
        try:
            result = self.user_model.update_user(user_id, data)
            if result:
                return dict(status_code=200, response='User updated successfully.')
            else:
                return dict(status_code=400, response='Could not update the user.')
        except Exception as e:
            return dict(status_code=500, response='Internal server error: ' + str(e))

    def delete_user(self, user_id):
        try:
            result = self.user_model.delete_user(user_id)
            if result:
                return dict(status_code=200, response='The user was successfully deleted.')
            else:
                return dict(status_code=400, response='Could not delete the user.')
        except Exception as e:
            return dict(status_code=500, response='Internal server error: ' + str(e))

    def search_users(self, criteria):
        try:
            result = self.user_model.search_users(criteria)
            if result:
                return dict(status_code=200, response=result)
            else:
                return dict(status_code=404, response='No users found with those criteria.')
        except Exception as e:
            return dict(status_code=500, response='Internal server error: ' + str(e))
