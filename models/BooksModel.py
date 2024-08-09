import psycopg2
from models.GeneralModel import GeneralModel
import logging


class BooksModel(GeneralModel):
    def __init__(self):
        super().__init__()
        self.table_name = 'books'

    def create_book(self, data):
        isbn = data.get('isbn')

        try:
            if self.check_duplicate_book(isbn):
                logging.info(f'The book with ISBN {isbn} already exists.')
            else:
                add_book = self.create(self.table_name, data)
                if add_book:
                    logging.info(f'Book inserted successfully.')
                else:
                    logging.error(f'Error inserting the book.')
        except psycopg2.Error as e:
            logging.error(f"Error creating the book: {e}")

    def check_duplicate_book(self, isbn):
        try:
            results = self.read(self.table_name, {'isbn': isbn})
            return bool(results)
        except psycopg2.Error as e:
            logging.error(f"Error verifying the duplicate book: {e}")

    def update_book_data(self, criteria, new_data):
        try:
            update_book_result = self.update(self.table_name, new_data, criteria)
            if update_book_result:
                logging.info(f'Book updated successfully.')
            else:
                logging.error(f'Error updating the book.')
        except psycopg2.Error as e:
            logging.error(f"Error updating the data: {e}")

    def delete_book(self, criteria):
        try:
            delete_book_result = self.delete(self.table_name, criteria)
            if delete_book_result:
                logging.info(f'Book deleted successfully.')
            else:
                logging.error(f'Error deleting the book.')
        except psycopg2.Error as e:
            logging.error(f"Error deleting the book: {e}")

    def query_books(self, criteria=None):
        try:
            if criteria:
                criteria_str = ", ".join([f"{key} = {value}" for key, value in criteria.items()])
                logging.info(f"\nQuerying books with criteria: '{criteria_str}'")
            else:
                logging.info("\nQuerying all books.")

            query_books_result = self.read(self.table_name, criteria)
            if query_books_result:
                for row in query_books_result:
                    print(row)
            else:
                logging.info("No results found.")
        except psycopg2.Error as e:
            logging.error(f"Error in the query: {e}")
