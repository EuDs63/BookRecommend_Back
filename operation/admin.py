from models.user import Users
from db_config import db_init as db


class admin_operation:
    def getAllUser(self):
        data = Users.query.all()
        return data
