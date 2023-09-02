from db_config import db_init as db

# Category 模型类
class Category(db.Model):
    # 表名
    __tablename__ = "categories"

    # 字段名
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name