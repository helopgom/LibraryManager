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
        print(f"No book_id found {book_id}.")

def update_book(self, book_id, title=None, author=None, quantity=None):
    """Updates the information of a book in the inventory."""
    for book in self.books:
        if book['book_id'] == book_id:
            if title:
                book['title'] = title
            if author:
                book['author'] = author
            if quantity is not None:
                book['quantity'] = quantity
            print(f"Booking_id {book_id} updated correctly.")
            return
    print(f"No book with ID found {book_id}.")


def list_books(self):
    """Shows the list of books in inventory."""
    if not self.books:
        print("Inventory is empty.")
        return
    for book in self.books:
        print(f"ID: {book['book_id']}, Títle: {book['title']}, Autor: {book['author']}, quantity: {book['quantity']}")


def search_book(self, book_id):
    """Searches for a book in the inventory by its ID."""
    for book in self.books:
        if book['book_id'] == book_id:
            print(
                f"Libro encontrado - ID: {book['book_id']}, Título: {book['title']}, Autor: {book['author']}, Cantidad: {book['quantity']}")
            return
    print(f"No book with ID found {book_id}.")




inventory = Inventory()
inventory.register_book(1, 'Cien Años de Soledad', 'Gabriel García Márquez', 10)
inventory.register_book(2, 'Don Quijote de la Mancha', 'Miguel de Cervantes', 5)
inventory.list_books()
inventory.update_book(1, quantity=12)
inventory.search_book(1)
inventory.remove_book(2)
inventory.list_books()