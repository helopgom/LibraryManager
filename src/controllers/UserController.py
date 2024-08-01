from models.UsersModel import UsersModel


class UserController:

    def __init__(self):
        self.user_model = UsersModel()

    def create_user(self, dni, user_name, user_lastname, mail, phone):
        try:
            if self.user_model.check_user_exists(dni):
                return dict(status_code=400,
                            response='Error: El usuario con este DNI ya existe.')

            success, error = self.user_model.create_user({
                'dni': dni,
                'name': user_name,
                'lastname': user_lastname,
                'email': mail,
                'phone': phone
            })
            if success:
                return dict(status_code=200,
                            response='El usuario fue creado de manera exitosa',
                            result=[dni, user_name, user_lastname, mail, phone])
            else:
                return dict(status_code=500,
                            response='Error al crear el usuario: ' + error,
                            error=error)
        except Exception as e:
            return dict(status_code=500,
                        response='Error interno del servidor: ' + str(e))

    def delete_user(self, user_id):
        try:
            success, error = self.user_model.delete_user({'id': user_id})
            if success:
                return dict(status_code=200,
                            response='El usuario fue eliminado de manera exitosa')
            else:
                return dict(status_code=500,
                            response='Error al eliminar el usuario',
                            error=error)
        except Exception as e:
            return dict(status_code=500,
                        response='Error interno del servidor: ' + str(e))

    def update_user(self, user_id, dni, user_name, user_lastname, mail, phone):
        try:
            success, error = self.user_model.update_user({
                'dni': dni,
                'name': user_name,
                'lastname': user_lastname,
                'email': mail,
                'phone': phone
            }, {'id': user_id})
            if success:
                return dict(status_code=200,
                            response='El usuario fue actualizado de manera exitosa',
                            result=[user_id, dni, user_name, user_lastname, mail, phone])
            else:
                return dict(status_code=500,
                            response='Error al actualizar el usuario',
                            error=error)
        except Exception as e:
            return dict(status_code=500,
                        response='Error interno del servidor: ' + str(e))

    def search_users(self, dni=None, user_name=None, user_lastname=None, mail=None, phone=None):
        try:
            results, error = self.user_model.get_user({
                'dni': dni,
                'name': user_name,
                'lastname': user_lastname,
                'email': mail,
                'phone': phone
            })
            if results:
                return dict(status_code=200,
                            response='Búsqueda exitosa',
                            result=results)
            else:
                return dict(status_code=404,
                            response='No se encontraron usuarios con los criterios especificados.')
        except Exception as e:
            return dict(status_code=500,
                        response='Error interno del servidor: ' + str(e))
