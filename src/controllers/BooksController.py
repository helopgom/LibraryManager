from models.BooksModel import BooksModel
import psycopg2


class BooksController:
    def __init__(self):
        self.book_model = BooksModel()

    def create_book(self, data):
        isbn = data.get('isbn')
        try:
            if self.check_duplicate_book(isbn):
                return dict(status_code=400, response=f'The book with ISBN {isbn} already exists.')
            else:
                add_book = self.book_model.create(self.book_model.table_name, data)
                if add_book:
                    return dict(status_code=200, response='Book inserted successfully.', result=data)
                else:
                    return dict(status_code=500, response='Error inserting the book.')
        except psycopg2.Error as e:
            return dict(status_code=500, response=f"Error creating the book: {e}")

    def check_duplicate_book(self, isbn):
        try:
            results = self.book_model.read(self.book_model.table_name, {'isbn': isbn})
            return bool(results)
        except psycopg2.Error as e:
            return dict(status_code=500, response=f"Error verifying the duplicate book: {e}")

    def update_book_data(self, criteria, new_data):
        try:
            update_book_result = self.book_model.update(self.book_model.table_name, new_data, criteria)
            if update_book_result:
                return dict(status_code=200, response='Book updated successfully.')
            else:
                return dict(status_code=500, response='Error updating the book.')
        except psycopg2.Error as e:
            return dict(status_code=500, response=f"Error updating the data: {e}")

    def delete_book(self, criteria):
        try:
            delete_book_result = self.book_model.delete(self.book_model.table_name, criteria)
            if delete_book_result:
                return dict(status_code=200, response='Book deleted successfully.')
            else:
                return dict(status_code=500, response='Error deleting the book.')
        except psycopg2.Error as e:
            return dict(status_code=500, response=f"Error deleting the book: {e}")

    def query_books(self, criteria=None):
        try:
            query_books_result = self.book_model.read(self.book_model.table_name, criteria)
            if query_books_result:
                return dict(status_code=200, response='Query successful.', result=query_books_result)
            else:
                return dict(status_code=404, response='No results found.')
        except psycopg2.Error as e:
            return dict(status_code=500, response=f"Error in the query: {e}")
