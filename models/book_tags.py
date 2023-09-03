from db_config import db_init as db

# BookCategory 模型类
class BookTag(db.Model):
    __tablename__ = 'book_tags'

    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)

    def __init__(self, book_id, tag_id):
        self.book_id = book_id
        self.tag_id = tag_id