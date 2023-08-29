from models.user import Users
from db_config import db_init as db


class user_operation:
    # def all(self):
    #     execute:select * from users
    #     data = Users.query.all()
    #     return  data
    def __init__(self):
        self.fields = ['user_id', 'username', 'register_time', 'is_admin']

    def getUserByUsername(self, username):
        user = Users.query.filter_by(username=username).first()
        return user
