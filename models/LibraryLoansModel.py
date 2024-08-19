
import psycopg2
import logging
from models.GeneralModel import GeneralModel
from psycopg2 import Error

class LibraryLoans(GeneralModel):
    def __init__(self):
        super().__init__()
        self.table = "library_loans"

    def create_loan(self, book_id_books, user_id_users, entry_date, return_date):
        try:

            query = f"SELECT MAX(loan_id) FROM {self.table}"
            result = self._execute_query(query, None, fetch=True)
            loan_id = (result[0][0] or 0) + 1


            loan_data = {
                "loan_id": loan_id,
                "book_id_books": book_id_books,
                "user_id_users": user_id_users,
                "entry_date": entry_date,
                "return_date": return_date
            }

            result = self.create(self.table, loan_data)
            return result

        except Exception as e:
            logging.error(f"Error creating the loan: {e}")
            return None


    # def read_loan(self, loan_id):
    #     try:
    #         # Lee un préstamo específico
    #         result = self.read(self.table, {"loan_id": loan_id})
    #         return result
    #
    #     except psycopg2.Error as e:
    #         logging.error(f"Error reading the loan: {e}")
    #         return None

    def read_loan(self, loan_id):
        try:
            query = f"SELECT * FROM {self.table} WHERE loan_id = %s"
            logging.info(f"Executing query: {query} with loan_id: {loan_id}")
            result = self._execute_query(query, (loan_id,), fetch=True)
            return result
        except psycopg2.Error as e:
            logging.error(f"Error reading the loan: {e}")
            return None

    def update_loan(self, loan_id, book_id_books=None, user_id_users=None, entry_date=None, return_date=None):
        try:
            # Verifica si el préstamo existe
            existing_loan = self.read_loan(loan_id)
            if not existing_loan:
                raise ValueError(f"Loan with ID {loan_id} not found.")

            # Actualiza el préstamo
            loan_data = {"book_id_books": book_id_books, "user_id_users": user_id_users, "entry_date": entry_date,
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
                    f"Book loan with ID {self.book_id_books} completed.")
            return rows_affected
        except Error as e:
            logging.error(f"Error finishing loan: {e}")
            return None

    def notify_return_date(self):
        try:
            logging.info(
                f"Book loan with ID {self.book_id_books} completed. Must be returned by the user with ID {self.user_id_users} before {self.return_date}.")
        except Error as e:
            logging.error(f"Error ending loan: {e}")

    def return_delay_alert(self):
        try:
            logging.info(
                f"Reminder: The book with ID {self.book_id_books} must be returned by the user with ID {self.user_id_users} before {self.return_date}.")
        except Error as e:
            logging.error(f"Error sending notification of return date: {e}")

    def notify_delay_date(self):
        try:
            logging.info(
                f"Alert: Book with ID {self.book_id_books} is delayed. The user with ID {self.user_id_users} was to be returned before {self.return_date}.")
        except Error as e:
            logging.error(f"Error sending delay notification: {e}")
