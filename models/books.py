from db_config import db_init as db
from datetime import datetime

class Books(db.Model):
    # 表名
    __tablename__ = 'books'
    # 字段名称
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    author = db.Column(db.String(64), nullable=False)
    publisher = db.Column(db.String(128), nullable=False)
    publish_date = db.Column(db.String(10), nullable=False)
    page_num = db.Column(db.Integer, nullable=False)
    cover_image_url = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rating_num = db.Column(db.Integer, default=0, nullable=False)
    rating_avg = db.Column(db.Numeric(3, 2), default=0.0, nullable=False)
    comment_count = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return '<Book %s>' % self.title
