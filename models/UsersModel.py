import psycopg2
from models.GeneralModel import GeneralModel
import logging


class UsersModel(GeneralModel):
    def __init__(self):
        super().__init__()
        self.table = "users"

    def check_user(self, data):
        try:
            query_dni = "SELECT * FROM {} WHERE dni = %s".format(self.table)
            params_dni = (data["dni"],)
            existing_user = self._execute_query(query_dni, params_dni, fetch=True)
            if existing_user:
                return logging.warning(f"A user with DNI {data['dni']} already exists.")

            query_email = "SELECT * FROM {} WHERE mail = %s".format(self.table)
            params_email = (data["mail"],)
            existing_email = self._execute_query(query_email, params_email, fetch=True)
            if existing_email:
                return logging.warning(f"A user with the email {data['mail']} already exists.")

            return None

        except psycopg2.Error as e:
            logging.error(f"Error verifying user: {e}")
            return "Error in user verification."

    def create_user(self, data):

        try:

            verification = self.check_user(data)
            if verification:
                raise ValueError(verification)

            result = self.create(self.table, data)
            return result

        except ValueError as ve:
            logging.error(ve)
            return None

        except psycopg2.Error as e:
            logging.error(f"Error creating the user: {e}")
            return None

    def update_user(self, user_id, data):
        try:
            existing_user = self.read(self.table, {"user_id": user_id})
            if not existing_user:
                raise ValueError(f"User with ID {user_id} not found.")

            if "mail" in data:
                conflicting_email = self.read(self.table, {"mail": data["mail"]})
                if conflicting_email and conflicting_email[0][0] != user_id:
                    raise ValueError(f"The email {data['mail']} is already in use by another user.")

            result = self.update(self.table, data, {"user_id": user_id})
            if result:
                return True
            return False

        except ValueError as ve:
            logging.error(ve)
            return None

        except psycopg2.Error as e:
            logging.error(f"Error updating the user: {e}")
            return None

    def delete_user(self, user_id):
        try:
            existing_user = self.read(self.table, {"user_id": user_id})
            if not existing_user:
                raise ValueError(f"User with ID {user_id} not found.")

            result = self.delete(self.table, {"user_id": user_id})
            return result

        except ValueError as ve:
            logging.error(ve)
            return None

        except psycopg2.Error as e:
            logging.error(f"Error deleting the user: {e}")
            return None

    def search_users(self, criteria):
        try:
            result = self.read(self.table, criteria)
            return result

        except psycopg2.Error as e:
            logging.error(f"Error searching for users: {e}")
            return None
