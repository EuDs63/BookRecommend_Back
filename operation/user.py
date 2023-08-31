from models.user import Users
from db_config import db_init as db


class user_operation:

    def __init__(self):
        self.fields = ['user_id', 'username', 'register_time', 'is_admin']

    def getUserByUsername(self, username):
        user = Users.query.filter_by(username=username).first()
        return user

    # 添加用户
    def addUser(self, username, password, register_time):
        # user = Users(username=username, password=password, register_time=register_time)
        user = Users(username=username, unencrypted_password=password, register_time=register_time)
        db.session.add(user)
        db.session.commit()
        return user


