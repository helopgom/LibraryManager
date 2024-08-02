from GeneralModel import GeneralModel
from psycopg2 import Error
import tim


class LibraryLoans(GeneralModel):
    def __init__(self, loan_id, book_id_books, user_id, entry_date, return_date):
        super().__init__()  # Inicializa la conexión de GeneralModel
        # Inicializa los atributos específicos de LibraryLoans
        self.loan_id = loan_id
        self.book_id_books = book_id_books
        self.user_id = user_id
        self.entry_date = entry_date
        self.return_date = return_date


    def avaible_loan(self,book_id_books):
        try :
            # verificamos si hay prestamos activos para el libro con el book_id_books dado
            loan = self.read("public.library_loans", {"book_id_books: book_id_books"})
            if loan:
                print(f"El libro con el ID{book_id_books} no está disponible.")
            else:
                print(f"El l ibro conID {book_id_books} está disponible.")
        except Error as e:
            print(f"Error al verificar la disponibilidad del libro: {e}")


    def register_loan(self):
        try:
            query = """
            INSERT INTO public.library_loans (loan_id, book_id_books, user_id_users, entry_date, return_date) 
            VALUES (%s, %s, %s, %s, %s) RETURNING loan_id
            """
            params = (self.loan_id, self.book_id_books, self.user_id, self.entry_date, self.return_date)
            loan_id = self._execute_query(query, params, fetch=True)
            if loan_id:
                self.loan_id = loan_id[0][0]  # Asignar el valor retornado
            return loan_id
        except Error as e:
            print(f"Error creating loan: {e}")

    def read_loan(self, loan_id):
        try:
            loan = self.read('public.library_loans', {'loan_id': loan_id})
            if loan:
                self.loan_id, self.book_id_books, self.user_id, self.entry_date, self.return_date = loan[0]
            return loan
        except Error as e:
            print(f"Error reading loan: {e}")

    def end_loan(self):
        try:
            rows_affected = self.delete('public.library_loans', {'loan_id': self.loan_id})
            if rows_affected:
                print(
                    f"Book loan with ID {self.book_id_books} completed. Must be returned by the user with ID {self.user_id} before {self.return_date}.")
            return rows_affected
        except Error as e:
            print(f"Error finishing loan: {e}")
            return None

    def notify_return_date(self, loan_id):
        try:
            time.sleep(5)  # Simulating a delay
            loan = self.read('public.library_loans', {'loan_id': loan_id})
            if loan:
                book_id_books, user_id, return_date = loan[0][1], loan[0][2], loan[0][4]
                print(
                    f"Reminder: The book with ID {book_id_books} must be returned by the user with ID {user_id} before {return_date}.")
            else:
                print(f"No loan found with ID {loan_id}.")
        except Error as e:
            print(f"Error fetching loan data: {e}")

    def notify_delay_date(self, loan_id):
        try:
            time.sleep(5)  # Simulating a delay
            loan = self.read('public.library_loans', {'loan_id': loan_id})
            if loan:
                book_id_books, user_id, return_date = loan[0][1], loan[0][2], loan[0][4]
                print(
                    f"Alert: Book with ID {book_id_books} is delayed. The user with ID {user_id} was to be returned before {return_date}.")
            else:
                print(f"No loan found with ID {loan_id}.")
        except Error as e:
            print(f"Error fetching loan data: {e}")
