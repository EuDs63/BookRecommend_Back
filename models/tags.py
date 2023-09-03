from db_config import db_init as db

# Category 模型类
class Tag(db.Model):
    # 表名
    __tablename__ = "tags"

    # 字段名
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), unique=True, nullable=False)

    def __init__(self, tag_name):
        self.tag_name = tag_name