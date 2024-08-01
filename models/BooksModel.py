from typing import Dict, Any
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
book.create('books', data)

