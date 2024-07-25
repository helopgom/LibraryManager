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

    def remove_book(self, book_id):
        for book in self.books:
            if book['book_id'] == book_id:
                self.books.remove(book)
                print(f"Libro con ID {book_id} eliminado con éxito.")
                return
        print(f"No se encontró ningún libro con ID {book_id}.")

inventory = Inventory()
inventory.register_book(1, 'Cien Años de Soledad', 'Gabriel García Márquez', 10)
inventory.register_book(2, 'Don Quijote de la Mancha', 'Miguel de Cervantes', 5)
inventory.remove_book(2)