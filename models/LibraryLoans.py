class LibraryLoans:
    def __init__(self,loan_id, book_id_books,user_id,entry_date,return_date):
        self.loan_id = loan_id
        self.book_id_books = book_id_books
        self.user_id = user_id
        self.entry_date = entry_date
        self.return_date = return_date

    def finish_loan(self):
        print(f"""Prestamo de libro {self.book.title} finalizado.
              Debe ser devuelto por {self.user_id.user_name} antes de {self.return_date})

