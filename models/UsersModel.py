from models.GeneralModel import GeneralModel
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class UsersModel(GeneralModel):
    def __init__(self):
        super().__init__()
        self.table = 'users'

    def check_user_exists(self, user_id):
        query = f"SELECT id FROM {self.table} WHERE id = %s"
        result = self._execute_query(query, [user_id], fetch=True)
        return len(result) > 0 if result else False

    def create_user(self, data):
        return self.create(self.table, data)

    def get_user(self, criteria):
        return self.read(self.table, criteria)

    def update_user(self, data, criteria):
        return self.update(self.table, data, criteria)

    def delete_user(self, criteria):
        return self.delete(self.table, criteria)