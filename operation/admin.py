from models.user import Users
from db_config import db_init as db


class admin_operation:
    # 获取并返回所有用户的信息
    def getAllUser(self):
        data = Users.query.all()
        return data

    # 添加管理员
    def addAdmin(self, username, password, register_time):
        admin = Users(username=username, unencrypted_password=password, register_time=register_time, is_admin=True)
        db.session.add(admin)
        db.session.commit()
        return admin
