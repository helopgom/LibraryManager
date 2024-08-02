from LibraryLoansModel import LibraryLoans

def get_user_loan_history(self, user_id):
    try:
        query = """
        SELECT loan_id, book_id_books, user_id_users, entry_date, return_date 
        FROM public.library_loans 
        WHERE user_id_users = %s
        ORDER BY entry_date DESC
        """
        params = (user_id,)
        loan_history = self._execute_query(query, params, fetch=True)
        return loan_history
    except Error as e:
        print(f"Error retrieving loan history: {e}")
        return None