from db_config import db_init as db
from datetime import datetime


class Books(db.Model):
    # 表名
    __tablename__ = 'books'
    # 字段名称
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20), nullable=False, default='')
    title = db.Column(db.String(256), nullable=False, default='')
    author = db.Column(db.String(64), nullable=False, default='')
    publisher = db.Column(db.String(128), nullable=False, default='')
    publish_date = db.Column(db.String(10), nullable=False, default='')
    page_num = db.Column(db.Integer, nullable=False, default=0)
    cover_image_url = db.Column(db.String(512), nullable=False, default='')
    description = db.Column(db.Text)
    rating_num = db.Column(db.Integer, nullable=False, default=0)
    rating_avg = db.Column(db.Numeric(3, 2), nullable=False, default=0.0)
    comment_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Book %s>' % self.title
