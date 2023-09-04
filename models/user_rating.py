from db_config import db_init as db

class UserRating(db.Model):
    __tablename__ = 'user_rating'

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    rating = db.Column(db.DECIMAL(2, 1), nullable=False)
    rating_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, user_id, book_id, rating):
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating
