from models.LibraryLoansModel import LibraryLoans
import psycopg2


class LoansController:
    def __init__(self):
        self.loans_model = LibraryLoans ()
    def create_loan(self, data):
        #registra un nuevo prestamo en el sistema
        try:
            loan_id = data.get('loan_id')
            book_id_books = data.get('book_id_books')
            user_id = data.get('user_id')
            entry_date = data.get('entry_date')
            return_date = data.get('return_date')

            # llama al metodo de models para registrar el prestamo
            loan_id_result = self.loans_model.create_loan(loan_id, book_id_books, user_id, entry_date, return_date)
            if loan_id_result:
                return dict(status_code=201, response="Loan registered successfully.", loan_id=loan_id_result)
            else:
                return dict(status_code=400, response="Could not register the loan.")
        except psycopg2.Error as e:
            return dict(status_code=500, response="Database error: " + str(e))
        except Exception as e:
            return dict(status_code=500, response="Internal server error: " + str(e))


    def read_loan(self, loan_id):
        #Consulta un préstamo existente por su ID.
        try:
            # Llamar al método del modelo para leer el préstamo
            loan = self.loans_model.read_loan(loan_id)
            if loan:
                return dict(status_code=200, response=loan)
            else:
                return dict(status_code=404, response="Loan not found.")
        except psycopg2.Error as e:
            return dict(status_code=500, response="Database error: " + str(e))
        except Exception as e:
            return dict(status_code=500, response="Internal server error: " + str(e))

    def update_loan(self, loan_id, data):
        #Actualiza los detalles de un préstamo existente.
        try:
            book_id_books = data.get('book_id_books')
            user_id = data.get('user_id')
            entry_date = data.get('entry_date')
            return_date = data.get('return_date')

            # Llamar al método del modelo para actualizar el préstamo
            rows_affected = self.loans_model.update_loan(loan_id, book_id_books, user_id, entry_date, return_date)
            if rows_affected:
                return dict(status_code=200, response="Loan updated successfully.")
            else:
                return dict(status_code=400, response="Could not update the loan.")
        except psycopg2.Error as e:
            return dict(status_code=500, response="Database error: " + str(e))
        except Exception as e:
            return dict(status_code=500, response="Internal server error: " + str(e))

    def delete_loan(self, loan_id):
        #Elimina un préstamo existente del sistema.
        try:
            # Llamar al método del modelo para eliminar el préstamo
            rows_affected = self.loans_model.delete_loan(loan_id)
            if rows_affected:
                return dict(status_code=200, response="Loan deleted successfully.")
            else:
                return dict(status_code=400, response="Could not delete the loan.")
        except psycopg2.Error as e:
            return dict(status_code=500, response="Database error: " + str(e))
        except Exception as e:
            return dict(status_code=500, response="Internal server error: " + str(e))
