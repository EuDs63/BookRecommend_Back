from models.books import Books
from models.categories import Category
from models.book_categories import BookCategory
from models.tags import Tag
from models.book_tags import BookTag
from db_config import db_init as db
import json
from logger import create_logger

logger = create_logger(__name__)


class book_operation:

    def __init__(self):
        self.basic_field = ['book_id', 'author', 'cover_image_url', 'title', 'rating_avg', 'description']
        self.known_categories = ["文学", "流行", "文化", "生活", "经管", "科技"]  # 类别已经确定为豆瓣所分的六大类，不再改动，所以硬编码

    # 根据book_id获取对应的book
    def getBookById(self, book_id):
        book = Books.query.filter_by(book_id=book_id).first()
        return book

    # 插入数据到books
    def insert_data_into_books(self, book_data):
        # 创建 Books 实例并插入到数据库books中
        book = Books(
            isbn=book_data['ISBN'],
            title=book_data["book_name"],
            rating_avg=float(book_data["score"]),
            comment_count=0,
            author=book_data["author_name"],
            publisher=book_data["press"],
            page_num=int(book_data["pages"]),
            publish_date=book_data["press_year"],
            cover_image_url=book_data["book_img"],
            rating_num=int(book_data["number_reviewers"]),
            description=book_data["introduction"],
        )
        db.session.add(book)
        db.session.flush()
        # 获取书籍的id
        book_id = book.book_id
        db.session.commit()
        return book_id

    # 插入数据到book_categories
    def insert_data_into_book_categories(self, book_id, category_str):
        # 创建一个类别映射字典
        category_mapping = {category: index + 1 for
                            index, category in enumerate(self.known_categories)}
        category_id = category_mapping.get(category_str, 1)
        book_category = BookCategory(book_id=book_id, category_id=category_id)
        db.session.add(book_category)
        # db.commit()

    def get_or_create_tag_id(self,tag_str):
        # 尝试在tags表中查找给定的tag_str
        tag = Tag.query.filter_by(tag_name=tag_str).first()

        # 如果找到了标签，则返回标签的tag_id
        if tag:
            return tag.tag_id
        else:
            # 否则，创建一个新的标签并返回其tag_id
            new_tag = Tag(tag_name=tag_str)
            db.session.add(new_tag)
            db.session.commit()
            return new_tag.tag_id

    def insert_data_into_book_tag(self,book_id, tag_str):
        tag_id = self.get_or_create_tag_id(tag_str)
        # 插入book_id和tag_id到book_tags表中
        book_tag = BookTag(book_id=book_id, tag_id=tag_id)
        db.session.add(book_tag)
        db.session.commit()

    # 从指定文件中读取数据，并录入到数据库中
    # 本函数执行后，四个表的数据会得到更新:books,book_categories,tags,book_tags
    # categories不更新原因：类别已经定好，本项目存续期间不会改变
    def load_books_to_database(self, json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            books_count = len(data)
            success_count = books_count

            for book_id in range(1, books_count + 1):
                book_data = data[str(book_id)]
                try:
                    book_id = self.insert_data_into_books(book_data)  # 插入数据到books
                    self.insert_data_into_book_categories(book_id, book_data["category"])  # 插入数据到book_categories
                    self.insert_data_into_book_tag(book_id, book_data["tag"])
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()  # 回滚事务，取消数据库更改
                    logger.error(f"导入数据库时发生异常: {e}")
                    success_count = success_count - 1
                    pass  # 跳过异常内容，继续执行后续代码

        return books_count, success_count
