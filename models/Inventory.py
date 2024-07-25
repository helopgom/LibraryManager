class Inventory:
    def __init__(self):
        self.books = {}
    def register_book(self, book_id, title, author, quantity):
        book = {
            'book_id': book_id,
            'title': title,
            'author': author,
            'quantity': quantity
        }
        self.books.append(book)
        print(f"Libro '{title}' registrado con éxito.")

inventory = Inventory()
inventory.register_book(1, 'Cien Años de Soledad', 'Gabriel García Márquez', 10)
