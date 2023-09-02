from models.book import Books
from db_config import db_init as db
import json
from logger import create_logger

logger = create_logger(__name__)


class book_operation:

    def __init__(self):
        self.basic_field = ['book_id', 'author', 'cover_image_url', 'title', 'rating_avg', 'description']

    def getBookById(self, book_id):
        book = Books.query.filter_by(book_id=book_id).first()
        return book

    def load_books_to_database(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            books_count = len(data)
            success_count = books_count

            for book_id in range(1, books_count + 1):
                book_data = data[str(book_id)]
                isbn = book_data['ISBN']
                title = book_data["book_name"]
                rating_avg = float(book_data["score"])
                author = book_data["author_name"]
                publisher = book_data["press"]
                page_num = int(book_data["pages"])
                publish_date = book_data["press_year"]
                cover_image_url = book_data["book_img"]
                rating_num = int(book_data["number_reviewers"])
                description = book_data["introduction"]
                try:
                    # 创建 Books 实例并插入到数据库
                    book = Books(
                        isbn=isbn,
                        title=title,
                        rating_avg=rating_avg,
                        comment_count=0,
                        author=author,
                        publisher=publisher,
                        page_num=page_num,
                        publish_date=publish_date,
                        cover_image_url=cover_image_url,
                        rating_num=rating_num,
                        description=description,
                    )
                    db.session.add(book)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()  # 回滚事务，取消数据库更改
                    logger.error(f"导入数据库时发生异常: {e}")
                    success_count = success_count-1
                    pass  # 继续执行后续代码

        return books_count,success_count
