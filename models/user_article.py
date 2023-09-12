from db_config import db_init as db

class UserArticle(db.Model):
    __tablename__ = 'user_article'

    article_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, book_id, user_id, content):
        self.book_id = book_id
        self.user_id = user_id
        self.content = content
