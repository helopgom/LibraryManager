class Inventory:
    def __init__(self):
        self.books = []

    def register_book(self, book_id, title, author, quantity):
        """Register a book in inventory."""
        book = {
            'book_id': book_id,
            'title': title,
            'author': author,
            'quantity': quantity
        }
        self.books.append(book)
        print(f"Libro '{title}' successfully registered.")
    def remove_book(self, book_id):
        """Removes a book from inventory by its ID."""
        for book in self.books:
            if book['book_id'] == book_id:
                self.books.remove(book)
                print(f"Book_id {book_id} successfully deleted.")
                return
        print(f"No book_id found {book_id}.")git
    def update_book(self, book_id, title=None, quantity=None):
        """Updates the information of a book in the inventory."""
        for book in self.books:
            if book[]




inventory = Inventory()
inventory.register_book(1, 'Cien Años de Soledad', 'Gabriel García Márquez', 10)
inventory.register_book(2, 'Don Quijote de la Mancha', 'Miguel de Cervantes', 5)
inventory.remove_book(2)