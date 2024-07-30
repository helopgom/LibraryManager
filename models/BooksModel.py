from models.GeneralModel import GeneralModel


class BooksModel(GeneralModel):
    def __init__(self):
        super().__init__()

data = {
'title': "Tierra",
'author': "Eloy Moreno",
'isbn': "123456",
'year_edition': "2022-12-12",
'category_id_categories': 1
}

book = BooksModel()

#Add book to the inventory
book_id = book.create('books', data)
if book_id:
    print(f'Libro insertado con ID: {book_id}')
else:
    print(f'Error al insertar el libro.')

