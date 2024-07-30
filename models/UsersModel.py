from models.BaseModel import BaseModel
import psycopg2


class UsersModel:
    def _init_(self):
        self.crud = BaseModel()

    def create_user(self, dni, user_name, user_lastname, mail, phone):
        query_check = "SELECT * FROM users WHERE dni = %s OR mail = %s"
        params_check = (dni, mail)
        try:
            with self.crud.connection.cursor() as cursor:
                cursor.execute(query_check, params_check)
                existing_user = cursor.fetchone()
                if existing_user:
                    return False, "Usuario ya existe con el mismo DNI o correo electrónico."

                data = {
                    'dni': dni,
                    'user_name': user_name,
                    'user_lastname': user_lastname,
                    'mail': mail,
                    'phone': phone
                }
                self.crud.create('users', data)
                return True, None
        except psycopg2.Error as e:
            print(f"Error al crear el usuario: {e}")
            return False, str(e)

    def delete_user(self, user_id):
        try:
            rows_deleted = self.crud.delete('users', {'user_id': user_id})
            if rows_deleted > 0:
                return True, None
            else:
                return False, "No se encontró el usuario con el ID proporcionado."
        except psycopg2.Error as e:
            print(f"Error al eliminar el usuario: {e}")
            return False, str(e)

    def update_user(self, user_id, dni, user_name, user_lastname, mail, phone):
        data = {
            'dni': dni,
            'user_name': user_name,
            'user_lastname': user_lastname,
            'mail': mail,
            'phone': phone
        }
        try:
            rows_updated = self.crud.update('users', data, {'user_id': user_id})
            if rows_updated > 0:
                return True, None
            else:
                return False, "No se encontró el usuario con el ID proporcionado."
        except psycopg2.Error as e:
            print(f"Error al actualizar el usuario: {e}")
            return False, str(e)

    def search_user(self, user_id=None, dni=None, user_name=None, user_lastname=None, mail=None, phone=None):
        criteria = {}
        if user_id:
            criteria['user_id'] = user_id
        if dni:
            criteria['dni'] = dni
        if user_name:
            criteria['user_name'] = user_name
        if user_lastname:
            criteria['user_lastname'] = user_lastname
        if mail:
            criteria['mail'] = mail
        if phone:
            criteria['phone'] = phone

        try:
            users = self.crud.read('users', criteria)
            return users
        except psycopg2.Error as e:
            print(f"Error al buscar usuarios: {e}")
            return []


# Instancia de UsersModel para ser utilizada en otros lugares
users_model = UsersModel()
