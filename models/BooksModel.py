from models.GeneralModel import GeneralModel

class BooksModel(GeneralModel):
    def __init__(self):
        super().__init__()
        self.table_name = 'books'
