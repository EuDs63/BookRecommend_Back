from db_config import db_init as db

# BookCategory 模型类
class BookCategory(db.Model):
    __tablename__ = 'book_categories'

    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)

    def __init__(self, book_id, category_id):
        self.book_id = book_id
        self.category_id = category_id