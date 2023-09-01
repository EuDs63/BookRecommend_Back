from models.book import Books
from db_config import db_init as db


class book_operation:

    def __init__(self):
        self.basic_field = ['book_id', 'author', 'cover_image_url', 'title', 'rating_avg', 'description']

    def getBookById(self, book_id):
        book = Books.query.filter_by(book_id=book_id).first()
        return book
