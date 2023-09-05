from models.users import Users
from db_config import db_init as db
from logger import create_logger

logger = create_logger(__name__)


class user_operation:

    def __init__(self):
        self.fields = ['user_id', 'username', 'register_time', 'is_admin', 'avatar_path']

    def getUserByUsername(self, username):
        user = Users.query.filter_by(username=username).first()
        return user

    def getUserByUserid(self, user_id):
        user = Users.query.filter_by(user_id=user_id).first()
        return user

    # 添加用户
    def addUser(self, username, password, register_time):
        # user = Users(username=username, password=password, register_time=register_time)
        user = Users(username=username, unencrypted_password=password, register_time=register_time)
        db.session.add(user)
        db.session.commit()
        return user

    def operation_change_avatar(self, user_id, avatar_path):
        try:
            user = self.getUserByUserid(user_id)
            user.avatar_path = avatar_path
            db.session.commit()
            return 0
        except Exception as e:
            db.session.rollback()
            logger.error(f"更改时发生异常: {e}")
            return -1
