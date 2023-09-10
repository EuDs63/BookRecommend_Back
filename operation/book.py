from sqlalchemy import desc

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
        self.detail_field = ['book_id', 'isbn', 'cover_image_url', 'title', 'author', 'publisher', 'rating_avg',
                             'publish_date', 'page_num', 'description', 'rating_num', 'comment_count']
        self.search_field = ['book_id', 'author', 'cover_image_url', 'title', 'rating_avg', 'description', 'publisher',
                             'publish_date']
        self.known_categories = ["文学", "流行", "文化", "生活", "经管", "科技"]  # 类别已经确定为豆瓣所分的六大类，不再改动，所以硬编码

    # 根据book_id获取对应的book
    def get_book_by_id(self, book_id):
        book = Books.query.filter_by(book_id=book_id).first()
        return book

    # 根据book_id获取其对应的category
    def get_category_by_book_id(self, book_id):
        # 查询book_categories表，获取与给定book_id相关的记录
        book_category_record = BookCategory.query.filter_by(book_id=book_id).all()
        # 获取book_category_record分别所对应的category_id
        category_ids = [record.category_id for record in book_category_record]
        # 根据category_id在category表查找对应的category
        categories = Category.query.filter(Category.category_id.in_(category_ids)).all()
        # 获取category对应的name
        category_name = [category.name for category in categories]
        return category_name

    # 根据book_id获取其对应的tag
    def get_tags_by_book_id(self, book_id):
        # 查询book_tags表，获取与给定book_id相关的记录
        book_tag_records = BookTag.query.filter_by(book_id=book_id).all()

        # 获取这些记录中的tag_id
        tag_ids = [record.tag_id for record in book_tag_records]

        # 使用tag_id查询tags表，获取标签名称
        tags = Tag.query.filter(Tag.tag_id.in_(tag_ids)).all()

        # 提取标签名称并返回
        tag_names = [tag.tag_name for tag in tags]
        return tag_names

    # 插入数据到books
    def insert_data_into_books(self, book_data):
        isbn = book_data['ISBN']  # 使用 ISBN 作为唯一标识符
        # 检查数据库中是否已经存在具有相同 ISBN 的书籍
        existing_book = Books.query.filter_by(isbn=isbn).first()
        if existing_book:
            book_id = existing_book.book_id
        else:  # 不存在
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
        category_id = category_mapping.get(category_str, 7)
        # 查找book_categories表中是否已经有重复的catagory、book_id
        book_category_record = BookCategory.query.filter_by(book_id=book_id, category_id=category_id).first()
        if book_category_record:
            pass
        else:  # 没有则添加
            book_category = BookCategory(book_id=book_id, category_id=category_id)
            db.session.add(book_category)

    def get_or_create_tag_id(self, tag_str):
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

    def insert_data_into_book_tag(self, book_id, tag_str):
        tag_id = self.get_or_create_tag_id(tag_str)
        # 在book_tag表中查找是否有重复的book_id、tag_id
        book_tag_record = BookTag.query.filter_by(book_id=book_id, tag_id=tag_id).first()
        if book_tag_record:
            pass
        else:
            # 插入book_id和tag_id到book_tags表中
            book_tag = BookTag(book_id=book_id, tag_id=tag_id)
            db.session.add(book_tag)

    # 从指定文件中读取数据，并录入到数据库中
    # 本函数执行后，四个表的数据会得到更新:books,book_categories,tags,book_tags
    # categories不更新原因：类别已经定好，本项目存续期间不会改变
    def load_books_to_database(self, json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            books_count = len(data)
            success_count = books_count

            for key, value in data.items():
                book_data = value
                try:
                    book_id = self.insert_data_into_books(book_data)  # 插入数据到books
                    self.insert_data_into_book_categories(book_id, book_data["category"])  # 插入数据到book_categories
                    self.insert_data_into_book_tag(book_id, book_data["tag"])
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()  # 回滚事务，取消数据库更改
                    logger.error(f"导入数据库时发生异常: {e}")
                    success_count = success_count - 1  # 这里的success_count是指没有进行异常处理的书，实际books表新增的书会少于这个数
                    pass  # 跳过异常内容，继续执行后续代码

            # for book_id in range(1, books_count + 1):
            #     book_data = data[str(book_id)]
            #     try:
            #         book_id = self.insert_data_into_books(book_data)  # 插入数据到books
            #         self.insert_data_into_book_categories(book_id, book_data["category"])  # 插入数据到book_categories
            #         self.insert_data_into_book_tag(book_id, book_data["tag"])
            #         db.session.commit()
            #     except Exception as e:
            #         db.session.rollback()  # 回滚事务，取消数据库更改
            #         logger.error(f"导入数据库时发生异常: {e}")
            #         success_count = success_count - 1  # 这里的success_count是指没有进行异常处理的书，实际books表新增的书会少于这个数
            #         pass  # 跳过异常内容，继续执行后续代码

        return books_count, success_count

    def insert_book_to_database(self,book_info):
        book_id = 0
        try:
            book_id = self.insert_data_into_books(book_info)  # 插入数据到books
            self.insert_data_into_book_categories(book_id, book_info["category"])  # 插入数据到book_categories
            self.insert_data_into_book_tag(book_id, book_info["tag"])
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # 回滚事务，取消数据库更改
            logger.error(f"导入数据库时发生异常: {e}")
            pass  # 跳过异常内容，继续执行后续代码
        return book_id

    # 根据category_id获取其对应的book
    def get_book_by_category_id(self, category_id):
        # 查询book_categories表，获取与给定category_id相关的记录
        book_category_record = BookCategory.query.filter_by(category_id=category_id).all()
        # 获取book_category_record分别所对应的book_id
        book_ids = [record.book_id for record in book_category_record]
        # 根据book_id在books表查找对应的book
        books = Books.query.filter(Books.book_id.in_(book_ids))
        return books

    # 根据tag_id获取其对应的book
    def get_book_by_tag_id(self, tag_id):
        # 查询book_tags表，获取与给定tag_id相关的记录
        book_tag_record = BookTag.query.filter_by(tag_id=tag_id).all()
        # 获取book_tag_record分别所对应的book_id
        book_ids = [record.book_id for record in book_tag_record]
        # 根据book_id在books表查找对应的book
        books = Books.query.filter(Books.book_id.in_(book_ids))
        return books

    # 按页返回所有书籍信息
    def return_all_book_infos(self, current_page, per_page):
        books_pagination = Books.query.paginate(page=current_page, per_page=per_page, error_out=False)
        return books_pagination

    # 分页返回特定category的所有书籍信息
    def return_category_book_infos(self, category_id, current_page, per_page,order):
        books = self.get_book_by_category_id(category_id)
        if order == 1:
            books = books.order_by(desc(Books.publish_date))
        elif order == 2:
            books = books.order_by(desc(Books.rating_num))
        books_pagination = books.paginate(page=current_page, per_page=per_page, error_out=False)
        return books_pagination

    # 分页返回特定tag的所有书籍信息
    def return_tag_book_infos(self, tag_id, current_page, per_page):
        books = self.get_book_by_tag_id(tag_id)
        books_pagination = books.paginate(page=current_page, per_page=per_page, error_out=False)
        return books_pagination

    # 分页返回搜索得到的所有书籍信息
    def return_searched_book_infos(self, keyword, current_page, per_page, method):
        if method == 1:
            books = Books.query.filter(
                (Books.title.ilike(f'%{keyword}%')) | (Books.author.ilike(f'%{keyword}%'))
            )
            books_pagination = books.paginate(page=current_page, per_page=per_page, error_out=False)
            return books_pagination

    def edit_info(self, book_id, edit_info):
        book = self.get_book_by_id(book_id)
        if book is not None:
            # 遍历 edit_info 中的字段，只更新出现的字段内容
            for key, value in edit_info.items():
                if hasattr(book, key):
                    if key == 'book_id':
                        pass  # book_id不允许修改
                    setattr(book, key, value)
            # 提交更新到数据库
            db.session.commit()
            return 0
        else:
            return -1
