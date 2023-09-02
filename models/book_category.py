from db_config import db_init as db

# BookCategory 模型类
class BookCategory(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)

    def __init__(self, book_id, category_id):
        self.book_id = book_id
        self.category_id = category_id