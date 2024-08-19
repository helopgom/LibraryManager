from models.BooksModel import BooksModel
from models.LibraryLoansModel import LibraryLoans
from models.UsersModel import UsersModel
from models.CategoriesModel import CategoriesModel
import logging
from logging_config import setup_logging



library_loan = LibraryLoans()
book = BooksModel()
user = UsersModel()
categories_model = CategoriesModel()

data_loan = {
    'book_id_books': 1,
    'user_id_users': 2,
    'entry_date': "2013-01-05",
    'return_date': "2013-01-12"
}

data_book = {
    'title': "Normal People",
    'author': "Sally Rooney",
    'isbn': "190011123",
    'year_edition': "2018-01-12",
    'category_id_categories': 2
}

new_user_data = {
    "dni": "13456879X",
    "user_name": "María",
    "user_lastname": "Estevez",
    "mail": "maria.estevez@example.com",
    "phone": "987654321"
}
# new_user_data = {
#     "dni": "87654321B",
#     "user_name": "Raquel",
#     "user_lastname": "Casado",
#     "mail": "raquelcasado@gmail.com",
#     "phone": "123456789"
# }

category_data = {
    'category_id': 1,
    'category_name': 'Ficción'
}

# categories_model.create_category(3, 'Poesía')

# categories_model.search_and_filter(1)

# categories_model.check_category(2)
#
# categories_model.update_category(3, 'Teatro')
#
# categories_model.delete_category(3)

#
# user.create_user(new_user_data)

# user.check_user()
#
# user.update_user()
#
# user.delete_user()
#
# user.search_users()
#
# if __name__ == "__main__":
# # Crear libro
# book.create_book(data_book)

# # Criterios para actualizar un libro y los nuevos datos
# update_criteria = {'category_id_categories': 3}
# new_data = {'category_id_categories': 1}
# book.update_book_data(update_criteria, new_data)

# # Eliminar un libro con un criterio específico (por ejemplo, por ISBN)
# delete_criteria = {'book_id': 21}
# book.delete_book(delete_criteria)

# # Consultar todos los libros
# book.query_books({'title': 'titulo consultado'})

# # Crear nuevo préstamo
#     library_loan.create_loan(3, 1, "2022-07-19", "2022-03-25")
