from models.users import Users
from db_config import db_init as db
from logger import create_logger

logger = create_logger(__name__)


class user_operation:

    def __init__(self):
        self.basic_field = ['username', 'register_time','avatar_path']
        self.detail_field = ['user_id', 'username', 'register_time', 'is_admin', 'avatar_path']

    def get_user_by_username(self, username):
        user = Users.query.filter_by(username=username).first()
        return user

    def get_user_by_userid(self, user_id):
        user = Users.query.filter_by(user_id=user_id).first()
        return user

    # 添加用户
    def add_user(self, username, password, register_time):
        # user = Users(username=username, password=password, register_time=register_time)
        user = Users(username=username, unencrypted_password=password, register_time=register_time)
        db.session.add(user)
        db.session.commit()
        return user

    def change_avatar(self, user_id, avatar_path):
        try:
            user = self.get_user_by_userid(user_id)
            user.avatar_path = avatar_path
            db.session.commit()
            return 0
        except Exception as e:
            db.session.rollback()
            logger.error(f"更改时发生异常: {e}")
            return -1
