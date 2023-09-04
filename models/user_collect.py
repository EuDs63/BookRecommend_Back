from db_config import db_init as db

class UserCollect(db.Model):
    __tablename__ = 'user_collect'

    collect_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    collect_type = db.Column(db.SmallInteger, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    collect_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, collect_type, user_id, book_id):
        self.collect_type = collect_type
        self.user_id = user_id
        self.book_id = book_id
