from models.BooksModel import BooksModel
from models.LibraryLoansModel import LibraryLoans

library_loan = LibraryLoans()
data = {
    'book_id_books': 1,
    'user_id_users': 2,
    'entry_date': "2013-01-05",
    'return_date': "2013-01-12"
}

book = BooksModel()
data2 = {
    'title': "nuevo libro",
    'author': "Esther",
    'isbn': "9100522",
    'year_edition': "2013-01-12",
    'category_id_categories': 1
}
if __name__ == "__main__":
    #book.create_book(data2)
    #library_loan.create_loan(3,2,"2013-06-05","2013-08-12")
    library_loan.read_loan()


