from config.DbConnection import Connection


class UsersModel:
    def __init__(self):
        self.db = Connection()

    def create_user(self, dni, user_name, user_lastname, mail, phone):
        query_check = "SELECT * FROM users WHERE dni = %s OR mail = %s"
        params_check = (dni, mail)
        try:
            existing_user = self.db.execute_query(query_check, params_check)
            if existing_user:
                return False, "Usuario ya existe con el mismo DNI o correo electrónico."

            query = "INSERT INTO users (dni, user_name, user_lastname, mail, phone) VALUES (%s, %s, %s, %s, %s)"
            params = (dni, user_name, user_lastname, mail, phone)
            self.db.execute_query(query, params)
            return True, None
        except Exception as e:
            return False, str(e)

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE user_id = %s"
        params = (user_id,)
        try:
            self.db.execute_query(query, params)
            return True, None
        except Exception as e:
            return False, str(e)

    def update_user(self, user_id, dni, user_name, user_lastname, mail, phone):
        query = """
        UPDATE users
        SET dni = %s, user_name = %s, user_lastname = %s, mail = %s, phone = %s
        WHERE user_id = %s
        """
        params = (dni, user_name, user_lastname, mail, phone, user_id)
        try:
            self.db.execute_query(query, params)
            return True, None
        except Exception as e:
            return False, str(e)

