from config.DbConnection import Connection
from psycopg2 import Error


class LibraryLoans:
    def __init__(self, loan_id, book_id_books, user_id, entry_date, return_date, ):
        self.loan_id = loan_id
        self.book_id_books = book_id_books
        self.user_id = user_id
        self.entry_date = entry_date
        self.return_date = return_date
        self.db = Connection()

    def register_loan(self):
        try:
            query = """
            INSERT INTO public.library_loans (loan_id, book_id_books, user_id_users, entry_date, return_date)
            VALUES (%s, %s, %s, %s) 
            RETURNING loan_id;
            """
            params = (self.loan_id, self.book_id_books, self.user_id, self.entry_date, self.return_date)
            loan_id = self.db.execute_query(query, params)
            if loan_id:
                self.loan_id = loan_id[0][0]
            return loan_id
        except Error as e:
            print(f"Error creating loan: {e}")

    def read_loan(self, loan_id):
        try:
            query = """
            SELECT loan_id, book_id_books, user_id_users, entry_date, return_date
             FROM public.library_loans
              WHERE loan_id = %s;
            """
            params = (loan_id,)
            loan = self.db.execute_query(query, params)
            if loan:
                self.loan_id, self.book_id_books, self.user_id, self.entry_date, self.return_date = loan[0]
            return loan
        except Error as e:
            print(f"Error reading loan: {e}")

    def update_loan(self):
        try:
            query = """
            UPDATE public.library_loans
            SET loan_id = %s, book_id_books = %s, user_id_users = %s, entry_date = %s, return_date = %s 
            WHERE loan_id = %s;
            """
            params = (self.loan_id, self.book_id_books, self.user_id, self.entry_date, self.return_date,)
            rows_affected = self.db.update_query(query, params)
            return rows_affected
        except Error as e:
            print(f"Error updating loan: {e}")

    def delete_loan(self):
        try:
            query = "DELETE FROM public.library_loans WHERE loan_id = %s;"
            params = (self.loan_id,)
            rows_affected = self.db.update_query(query, params)
            return rows_affected
        except Error as e:
            print(f"Error deleting loan: {e}")
            return None

    def end_loan(self):
        try:
            rows_affected = self.delete_loan()
            if rows_affected:
                print(
                    f"Book loan with ID {self.book_id_books} completed. Must be returned by the user with ID {self.user_id} before {self.return_date}.")
            return rows_affected
        except Error as e:
            print(f"Error finishing loan: {e}")
            return None

    def notify_return_date(self):
        try:
            print(
                f"Book loan with ID {self.book_id_books} completed. Must be returned by the user with ID {self.user_id} before {self.return_date}.")
        except Error as e:
            print(f"Error ending loan: {e}")

    def return_delay_alert(self):
        try:
            print(
                f"Reminder: The book with ID {self.book_id_books} must be returned by the user with ID {self.user_id} before {self.return_date}.")
        except Error as e:
            print(f"Error sending notification of return date: {e}")

    def notify_delay_date(self):
        try:
            print(
                f"Alert: Book with ID {self.book_id_books} is delayed. The user with ID {self.user_id} was to be returned before {self.return_date}.")
        except Error as e:
            print(f"Error sending delay notification: {e}")
