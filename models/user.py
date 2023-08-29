from db_config import db_init as db


# 定义user数据模型类
class Users(db.Model):
    # 表名
    __tablename__ = 'users'
    # 字段名称
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    register_time = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<User %s>' % self.username
