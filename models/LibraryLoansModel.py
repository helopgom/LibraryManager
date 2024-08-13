import psycopg2
from models.GeneralModel import GeneralModel
from psycopg2 import Error
import logging


class LibraryLoans(GeneralModel):
    def __init__(self):
        super().__init__()
        self.book_id_books = "book_id_books"
        self.table = "library_loans"

    def create_loan(self, loan_id, book_id_books, user_id, entry_date, return_date):
        try:
            # Verifica si ya existe un préstamo con el mismo ID
            existing_loan = self.read_loan(loan_id)
            if existing_loan:
                raise ValueError(f"A loan with ID {loan_id} already exists.")

            # Crear un nuevo préstamo

            loan_data = {"loan_id": loan_id, "book_id_books": book_id_books, "user_id_users": user_id,
                         "entry_date": entry_date, "return_date": return_date}

            result = self.create(self.table, loan_data)
            return result

        except ValueError as ve:
            logging.error(ve)
            return None

        except psycopg2.Error as e:
            logging.error(f"Error creating the loan: {e}")
            return None

    def read_loan(self, loan_id):
        try:
            # Lee un préstamo específico
            result = self.read(self.table, {"loan_id": loan_id})
            return result

        except psycopg2.Error as e:
            logging.error(f"Error reading the loan: {e}")
            return None

    def update_loan(self, loan_id, book_id_books=None, user_id=None, entry_date=None, return_date=None):
        try:
            # Verifica si el préstamo existe
            existing_loan = self.read_loan(loan_id)
            if not existing_loan:
                raise ValueError(f"Loan with ID {loan_id} not found.")

            # Actualiza el préstamo
            loan_data = {"book_id_books": book_id_books, "user_id_users": user_id, "entry_date": entry_date,
                         "return_date": return_date}

            # Filtra None para no actualizar campos vacíos
            loan_data = {key: value for key, value in loan_data.items() if value is not None}

            result = self.update(self.table, loan_data, {"loan_id": loan_id})
            return result

        except ValueError as ve:
            logging.error(ve)
            return None

        except psycopg2.Error as e:
            logging.error(f"Error updating the loan: {e}")
            return None

    def delete_loan(self, loan_id):
        try:
            # Verifica si el préstamo existe
            existing_loan = self.read_loan(loan_id)
            if not existing_loan:
                raise ValueError(f"Loan with ID {loan_id} not found.")

                # Elimina el préstamo
                result = self.delete(self.table, {"loan_id": loan_id})
                return result

        except ValueError as ve:
            logging.error(ve)
            return None

        except psycopg2.Error as e:
            logging.error(f"Error deleting the loan: {e}")
            return None

    def end_loan(self):
        try:
            rows_affected = self.delete_loan()
            if rows_affected:
                logging.info(
                    f"Book loan with ID {self.book_id_books} completed. Must be returned by the user with ID {self.user_id} before {self.return_date}.")
            return rows_affected
        except Error as e:
            logging.error(f"Error finishing loan: {e}")
            return None

    def notify_return_date(self):
        try:
            logging.info(
                f"Book loan with ID {self.book_id_books} completed. Must be returned by the user with ID {self.user_id} before {self.return_date}.")
        except Error as e:
            logging.error(f"Error ending loan: {e}")

    def return_delay_alert(self):
        try:
            logging.info(
                f"Reminder: The book with ID {self.book_id_books} must be returned by the user with ID {self.user_id} before {self.return_date}.")
        except Error as e:
            logging.error(f"Error sending notification of return date: {e}")

    def notify_delay_date(self):
        try:
            logging.info(
                f"Alert: Book with ID {self.book_id_books} is delayed. The user with ID {self.user_id} was to be returned before {self.return_date}.")
        except Error as e:
            logging.error(f"Error sending delay notification: {e}")
