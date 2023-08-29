from models.user import Users
from db_config import db_init as db


class user_operation:
    #     def all(self):
    #     execute:select * from users

    def login(self, username, password):
        user = Users.query.filter_by(username=username).first()
        print(user.username)
        print(user.password)
        return user
