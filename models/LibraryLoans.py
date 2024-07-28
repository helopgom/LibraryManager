
class LibraryLoans:
    def __init__(self, loan_id=None, book_id_books=None, user_id=None, entry_date=None, return_date=None):
        self.loan_id = loan_id
        self.book_id_books = book_id_books
        self.user_id = user_id
        self.entry_date = entry_date
        self.return_date = return_date

    def create_loan(self, connection):
        try:
            query = """
            INSERT INTO library_loans (book_id_books, user_id_users, entry_date, return_date)
            VALUES (%s, %s, %s, %s) RETURNING loan_id;
            """
            params = (self.book_id_books, self.user_id, self.entry_date, self.return_date)
            loan_id = connection.execute_query(query, params)
            if loan_id:
                self.loan_id = loan_id[0][0]
            return loan_id
        except Error as e:
            print(f"Error creando el préstamo: {e}")

    def read_loan(self, connection, loan_id):
        try:
            query = "SELECT * FROM library_loans WHERE loan_id = %s;"
            params = (loan_id,)
            loan = connection.execute_query(query, params)
            if loan:
                self.loan_id, self.book_id_books, self.user_id, self.entry_date, self.return_date = loan[0]
            return loan
        except Error as e:
            print(f"Error leyendo el préstamo: {e}")

    def update_loan(self, connection):
        try:
            query = """
            UPDATE library_loans
            SET book_id_books = %s, user_id_users = %s, entry_date = %s, return_date = %s
            WHERE loan_id = %s;
            """
            params = (self.book_id_books, self.user_id, self.entry_date, self.return_date, self.loan_id)
            rows_affected = connection.update_query(query, params)
            return rows_affected
        except Error as e:
            print(f"Error actualizando el préstamo: {e}")

    def delete_loan(self, connection):
        try:
            query = "DELETE FROM library_loans WHERE loan_id = %s;"
            params = (self.loan_id,)
            rows_affected = connection.update_query(query, params)
            return rows_affected
        except Error as e:
            print(f"Error eliminando el préstamo: {e}")

    def finish_loan(self):
        try:
            print(f"Préstamo de libro con ID {self.book_id_books} finalizado. Debe ser devuelto por el usuario con ID {self.user_id} antes de {self.return_date}.")
        except Error as e:
            print(f"Error finalizando el préstamo: {e}")

    def notify_due_date(self):
        try:
            print(f"Recordatorio: El libro con ID {self.book_id_books} debe ser devuelto por el usuario con ID {self.user_id} antes de {self.return_date}.")
        except Error as e:
            print(f"Error enviando notificación de fecha de devolución: {e}")

    def notify_overdue(self):
        try:
            print(f"Alerta: El libro con ID {self.book_id_books} está retrasado. El usuario con ID {self.user_id} debía devolverlo antes de {self.return_date}.")
        except Error as e:
            print(f"Error enviando notificación de retraso: {e}")

