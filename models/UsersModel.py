import psycopg2
from models.GeneralModel import GeneralModel
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


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
                return f"Ya existe un usuario con el DNI {data['dni']}"

            # Construir consulta para verificar por correo electrónico
            query_email = "SELECT * FROM {} WHERE mail = %s".format(self.table)
            params_email = (data["mail"],)
            existing_email = self._execute_query(query_email, params_email, fetch=True)
            if existing_email:
                return f"Ya existe un usuario con el correo {data['mail']}"

            return None  # No hay conflictos, se puede proceder

        except psycopg2.Error as e:
            logger.error(f"Error al verificar usuario: {e}")
            return "Error en la verificación de usuario."

    def create_user(self, data):
        """Crea un nuevo usuario después de verificar que no haya duplicados."""
        try:
            # Verificar si ya existe un usuario con el mismo DNI o correo
            verificacion = self.check_user(data)
            if verificacion:
                raise ValueError(verificacion)

            # Registrar el nuevo usuario si no hay conflictos
            result = self.create(self.table, data)
            return result

        except ValueError as ve:
            logger.error(ve)
            return None

        except psycopg2.Error as e:  # Captura todas las excepciones relacionadas con psycopg2
            logger.error(f"Error al crear el usuario: {e}")
            return None

    def update_user(self, user_id, data):
        try:
            # Validar si existe el usuario a actualizar
            existing_user = self.read(self.table, {"user_id": user_id})
            if not existing_user:
                return None  # Retorna None si no se encuentra el usuario

            # Verificar si el nuevo correo pertenece a otro usuario
            if "mail" in data:
                conflicting_email = self.read(self.table, {"mail": data["mail"]})
                if conflicting_email and conflicting_email[0][0] != user_id:
                    return None  # Retorna None si el correo está en uso

            # Actualizar la información del usuario
            result = self.update(self.table, data, {"user_id": user_id})
            return True if result else None  # Retorna True si la actualización fue exitosa, None si no

        except ValueError as ve:
            logger.error(ve)
            return None

        except psycopg2.Error as e:
            logger.error(f"Error al actualizar el usuario: {e}")
            return None

    def delete_user(self, user_id):
        try:
            # Validar si existe el usuario a eliminar
            existing_user = self.read(self.table, {"user_id": user_id})
            if not existing_user:
                raise ValueError(f"No se encontró el usuario con ID {user_id}")

            # Eliminar el usuario
            result = self.delete(self.table, {"user_id": user_id})
            return result

        except ValueError as ve:
            logger.error(ve)
            return None

        except psycopg2.Error as e:  # Captura todas las excepciones relacionadas con psycopg2
            logger.error(f"Error al eliminar el usuario: {e}")
            return None

    def search_users(self, criteria):
        try:
            # Buscar usuarios según los criterios proporcionados
            result = self.read(self.table, criteria)
            return result

        except psycopg2.Error as e:  # Captura todas las excepciones relacionadas con psycopg2
            logger.error(f"Error al buscar usuarios: {e}")
            return None
