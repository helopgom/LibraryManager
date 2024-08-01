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
            # Verificar por DNI
            existing_user = self.read(self.table, {"dni": data["dni"]})
            if existing_user:
                return f"Ya existe un usuario con el DNI {data['dni']}"

            # Verificar por correo electrónico
            existing_email = self.read(self.table, {"mail": data["mail"]})
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
                raise ValueError(f"No se encontró el usuario con ID {user_id}")

            # Verificar si el nuevo correo pertenece a otro usuario
            if "mail" in data:
                conflicting_email = self.read(self.table, {"mail": data["mail"]})
                if conflicting_email and conflicting_email[0][0] != user_id:
                    raise ValueError(f"El correo {data['mail']} ya está en uso por otro usuario.")

            # Actualizar la información del usuario
            result = self.update(self.table, data, {"user_id": user_id})
            return result

        except ValueError as ve:
            logger.error(ve)
            return None

        except psycopg2.Error as e:  # Captura todas las excepciones relacionadas con psycopg2
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
