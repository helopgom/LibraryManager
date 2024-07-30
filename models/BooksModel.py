from typing import Dict, Any
from models.GeneralModel import GeneralModel


class BooksModel(GeneralModel):

    def __init__(self):
        super().__init__()


data = {}
book = BooksModel()
book.create('books', data)

