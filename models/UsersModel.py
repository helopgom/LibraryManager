import psycopg2
from models.GeneralModel import GeneralModel
import logging


class UsersModel(GeneralModel):
    def __init__(self):
        super().__init__()
        self.table = "users"

    def check_user(self, data):
        """Verifica si ya existe un usuario con el mismo DNI o correo."""
        try:
            # Construir consulta para verificar por DNI
            query_dni = "SELECT * FROM {} WHERE dni = %s".format(self.table)
            params_dni = (data["dni"],)
            existing_user = self._execute_query(query_dni, params_dni, fetch=True)
            if existing_user:
                return f"A user with DNI {data['dni']} already exists."

            # Construir consulta para verificar por correo electrónico
            query_email = "SELECT * FROM {} WHERE mail = %s".format(self.table)
            params_email = (data["mail"],)
            existing_email = self._execute_query(query_email, params_email, fetch=True)
            if existing_email:
                return f"A user with the email {data['mail']} already exists."

            return None  # No hay conflictos, se puede proceder

        except psycopg2.Error as e:
            logging.error(f"Error verifying user: {e}")
            return "Error in user verification."

    def create_user(self, data):
        """Crea un nuevo usuario después de verificar que no haya duplicados."""
        try:
            # Verificar si ya existe un usuario con el mismo DNI o correo
            verification = self.check_user(data)
            if verification:
                raise ValueError(verification)

            # Registrar el nuevo usuario si no hay conflictos
            result = self.create(self.table, data)
            return result

        except ValueError as ve:
            logging.error(ve)
            return None

        except psycopg2.Error as e:  # Captura todas las excepciones relacionadas con psycopg2
            logging.error(f"Error creating the user: {e}")
            return None

    def update_user(self, user_id, data):
        try:
            # Validar si existe el usuario a actualizar
            existing_user = self.read(self.table, {"user_id": user_id})
            if not existing_user:
                raise ValueError(f"User with ID {user_id} not found.")

            # Verificar si el nuevo correo pertenece a otro usuario
            if "mail" in data:
                conflicting_email = self.read(self.table, {"mail": data["mail"]})
                if conflicting_email and conflicting_email[0][0] != user_id:
                    raise ValueError(f"The email {data['mail']} is already in use by another user.")

            # Actualizar la información del usuario
            result = self.update(self.table, data, {"user_id": user_id})
            if result:
                return True  # Retorna True si la actualización fue exitosa
            return False  # Retorna None si la actualización no fue exitosa

        except ValueError as ve:
            logging.error(ve)
            return None  # Retorna None en caso de un error de valor

        except psycopg2.Error as e:
            logging.error(f"Error updating the user: {e}")
            return None  # Retorna None en caso de un error de base de datos

    def delete_user(self, user_id):
        try:
            # Validar si existe el usuario a eliminar
            existing_user = self.read(self.table, {"user_id": user_id})
            if not existing_user:
                raise ValueError(f"User with ID {user_id} not found.")

            # Eliminar el usuario
            result = self.delete(self.table, {"user_id": user_id})
            return result

        except ValueError as ve:
            logging.error(ve)
            return None

        except psycopg2.Error as e:  # Captura todas las excepciones relacionadas con psycopg2
            logging.error(f"Error deleting the user: {e}")
            return None

    def search_users(self, criteria):
        try:
            # Buscar usuarios según los criterios proporcionados
            result = self.read(self.table, criteria)
            return result

        except psycopg2.Error as e:  # Captura todas las excepciones relacionadas con psycopg2
            logging.error(f"Error searching for users: {e}")
            return None
