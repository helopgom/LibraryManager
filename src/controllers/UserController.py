from models.UsersModel import UsersModel

class UserController:
    def __init__(self):
        self.user_model = UsersModel()

    def check_user(self, data):
        try:
            verification_message = self.user_model.check_user(data)
            if verification_message:
                return dict(status_code=400, response=verification_message)
            return dict(status_code=200, response='Verificación exitosa, el usuario puede ser creado')
        except Exception as e:
            return dict(status_code=500, response='Error interno del servidor: ' + str(e))

    def create_user(self, data):
        try:
            verification_response = self.check_user(data)
            if verification_response['status_code'] != 200:
                return verification_response

            result = self.user_model.create_user(data)
            if result:
                return dict(status_code=201, response='Usuario creado con éxito')
            else:
                return dict(status_code=400, response='No se pudo crear el usuario')
        except Exception as e:
            return dict(status_code=500, response='Error interno del servidor: ' + str(e))

    def update_user(self, user_id, data):
        try:
            result = self.user_model.update_user(user_id, data)
            if result:
                return dict(status_code=200, response='Usuario actualizado con éxito')
            else:
                return dict(status_code=400, response='No se pudo actualizar el usuario')
        except Exception as e:
            return dict(status_code=500, response='Error interno del servidor: ' + str(e))

    def delete_user(self, user_id):
        try:
            result = self.user_model.delete_user(user_id)
            if result:
                return dict(status_code=200, response='El usuario fue eliminado de manera exitosa')
            else:
                return dict(status_code=400, response='No se pudo eliminar el usuario')
        except Exception as e:
            return dict(status_code=500, response='Error interno del servidor: ' + str(e))

    def search_users(self, criteria):
        try:
            result = self.user_model.search_users(criteria)
            if result:
                return dict(status_code=200, response=result)
            else:
                return dict(status_code=404, response='No se encontraron usuarios con esos criterios')
        except Exception as e:
            return dict(status_code=500, response='Error interno del servidor: ' + str(e))
