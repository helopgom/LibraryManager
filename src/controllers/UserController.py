from models.UsersModel import UsersModel


class UserController:

    def __init__(self):
        self.user_model = UsersModel()

    def create_user(self, dni, user_name, user_lastname, mail, phone):
        try:
            success, error = self.user_model.create_user(dni, user_name, user_lastname, mail, phone)
            if success:
                return dict(status_code=200,
                            response='El usuario fue creado de manera exitosa',
                            result=[dni, user_name, user_lastname, mail, phone])
            else:
                return dict(status_code=400,
                            response='Error al crear el usuario: ' + error,
                            error=error)
        except Exception as e:
            return dict(status_code=500,
                        response='Error interno del servidor: ' + str(e))

    def delete_user(self, user_id):
        success, error = self.user_model.delete_user(user_id)
        if success:
            return dict(status_code=200,
                        response='El usuario fue eliminado de manera exitosa')
        else:
            return dict(status_code=500,
                        response='Error al eliminar el usuario',
                        error=error)

    def update_user(self, user_id, dni, user_name, user_lastname, mail, phone):
        success, error = self.user_model.update_user(user_id, dni, user_name, user_lastname, mail, phone)
        if success:
            return dict(status_code=200,
                        response='El usuario fue actualizado de manera exitosa',
                        result=[user_id, dni, user_name, user_lastname, mail, phone])
        else:
            return dict(status_code=500,
                        response='Error al actualizar el usuario',
                        error=error)
