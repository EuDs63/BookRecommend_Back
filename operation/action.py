from models.user_rating import UserRating
from models.user_collect import UserCollect
from models.user_comment import UserComment
from models.user_article import UserArticle
from models.users import Users
from operation.book import book_operation
from db_config import db_init as db
import json
from logger import create_logger
from models.books import Books
from utils.data_process import Data_Process, Paginate_Process
from sqlalchemy import desc

logger = create_logger(__name__)


class action_operation:
    def __init__(self):
        self.action_type = ['user_collect', 'user_comment', 'user_rating', 'user_article']
        self.article_field = ['article_id', 'book_id', 'user_id', 'content', 'article_title', 'create_time']

    def add_user_collect(self, user_id, book_id, content):
        user_collect = UserCollect(user_id=user_id, book_id=book_id, collect_type=content)
        db.session.add(user_collect)

    def add_user_comment(self, user_id, book_id, content):
        b = book_operation()
        book = b.get_book_by_id(book_id)
        book.comment_count = book.comment_count + 1
        user_comment = UserComment(user_id=user_id, book_id=book_id, content=content)
        db.session.add(book)
        db.session.add(user_comment)

    def add_user_rating(self, user_id, book_id, content):
        user_rating = UserRating(user_id=user_id, book_id=book_id, rating=content)
        db.session.add(user_rating)

    def add_user_article(self, user_id, book_id, content, article_title):
        user_article = UserArticle(user_id=user_id, book_id=book_id, content=content, article_title=article_title)
        db.session.add(user_article)

    def get_user_collect_records(self, method, user_id, book_id, current_page, page_size):
        result = []
        if method == 2:
            # 查询用户收藏的书籍、收藏类型和书籍标题
            user_collect_records = db.session.query(UserCollect, Books) \
                .join(Books, UserCollect.book_id == Books.book_id) \
                .filter(UserCollect.user_id == user_id)

            # 按照收藏时间从新到旧的顺序进行排列
            user_collect_records = user_collect_records.order_by(desc(UserCollect.collect_time))
            # 进行分页处理，每页5个
            user_collect_records = user_collect_records.paginate(page=current_page, per_page=page_size, error_out=False)

            for user_collect, book in user_collect_records:
                b = book_operation()
                book_info = Data_Process(book, b.basic_field, 1)
                result.append({
                    'book': book_info,
                    'collect_type': user_collect.collect_type,
                    'collect_time': user_collect.collect_time.strftime('%Y-%m-%d %H:%M:%S'),  # 格式化时间
                })
        return result

    # 获取收藏同本书的人的信息
    def get_collect_members(self, book_id):
        members = []
        # 查询收藏了该书的用户、收藏类型和时间，并获取用户名
        user_collect_records = db.session.query(UserCollect, Users) \
            .join(Users, UserCollect.user_id == Users.user_id) \
            .filter(UserCollect.book_id == book_id)

        # 按照收藏时间从新到旧的顺序进行排列
        user_collect_records = user_collect_records.order_by(desc(UserCollect.collect_time))

        # 创建一个集合用于存储已经出现过的 book_id
        seen_user_ids = set()

        for user_collect, user in user_collect_records:
            if user is not None:
                # 进行判断，如果之前已经出现，则不添加
                # 判断 user_id 是否已经出现过，如果没有则添加到结果列表中
                if user.user_id not in seen_user_ids:
                    seen_user_ids.add(user.user_id)
                    members.append({
                        'img': user.avatar_path,
                        'name': user.username
                    })
            # 当 members 的长度达到 4 时，停止添加
            if len(members) >= 4:
                break

        return members

    def get_user_collect(self, method, user_id, book_id, current_page):
        # 构建结果字典列表
        result = []
        if method == 1:  # 根据 book_id 查找收藏该书的用户、以及收藏类型、时间 (user_id 在collect_time将本书添加到了collect_type)
            # 查询收藏了该书的用户、收藏类型和时间，并获取用户名
            user_collect_records = db.session.query(UserCollect, Users) \
                .join(Users, UserCollect.user_id == Users.user_id) \
                .filter(UserCollect.book_id == book_id)

            # 按照收藏时间从新到旧的顺序进行排列
            user_collect_records = user_collect_records.order_by(desc(UserCollect.collect_time))
            # 进行分页处理，每页5个
            user_collect_records = user_collect_records.paginate(page=current_page, per_page=5, error_out=False)

            for user_collect, user in user_collect_records:
                result.append({
                    'user_id': user_collect.user_id,
                    'username': user.username,
                    'avatar_path': user.avatar_path,
                    'collect_type': user_collect.collect_type,
                    'collect_time': user_collect.collect_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
                })
        elif method == 2:  # 根据 user_id 查找该user收藏了哪些书，收藏的类型 （在collect_time将book_id添加到了collect_type
            # 查询用户收藏的书籍、收藏类型和书籍标题
            user_collect_records = db.session.query(UserCollect, Books) \
                .join(Books, UserCollect.book_id == Books.book_id) \
                .filter(UserCollect.user_id == user_id)

            # 按照从新到旧进行排序
            user_collect_records = user_collect_records.order_by(desc(UserCollect.collect_time))

            # 创建一个集合用于存储已经出现过的 book_id
            seen_book_ids = set()

            b = book_operation()

            for user_collect, book in user_collect_records:
                # 进行判断，如果之前已经出现，则不添加
                # 判断 book_id 是否已经出现过，如果没有则添加到结果列表中
                if book.book_id not in seen_book_ids:
                    # 将当前的 book_id 添加到集合中，以便后续判断
                    seen_book_ids.add(book.book_id)
                    # 添加到返回数据中
                    book_info = Data_Process(book, b.search_field, 1)
                    result.append({
                        'book': book_info,
                        'collect_type': user_collect.collect_type,
                        'collect_time': user_collect.collect_time.strftime('%Y-%m-%d %H:%M:%S'),  # 格式化时间
                    })
        elif method == 3:  # 根据 book_id 和 user_id 查找收藏内容 (在collect_time,添加到了collect_type
            user_collect = UserCollect.query.filter_by(user_id=user_id, book_id=book_id)

            # 按照收藏时间从新到旧的顺序进行排列
            user_collect = user_collect.order_by(desc(UserCollect.collect_time))
            # 进行分页处理，每页5个
            user_collect = user_collect.paginate(page=current_page, per_page=5, error_out=False)
            for collect_record in user_collect:
                result.append({
                    'collect_type': collect_record.collect_type,
                    'collect_time': collect_record.collect_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
                })
        else:  # 处理无效的 method 参数
            logger.error("无效的 method 参数: {}".format(method))
        return result

    def get_user_comment(self, method, user_id, book_id):
        # 构建结果字典列表
        result = []

        if method == 1:  # 根据 book_id 查找该书的评论用户、以及评论内容和时间 (user_id 在create_time对book_id发表了评论)
            user_comment_records = db.session.query(UserComment, Users) \
                .join(Users, UserComment.user_id == Users.user_id) \
                .filter(UserComment.book_id == book_id) \
                .all()
            # 这里的comment_id与数据库中的不同
            comment_id = 1
            for user_comment, user in user_comment_records:
                result.append({
                    'comment_id': comment_id,
                    'user_id': user_comment.user_id,
                    'username': user.username,
                    'avatar_path': user.avatar_path,
                    'content': user_comment.content,
                    'create_time': user_comment.create_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
                })
                comment_id = comment_id + 1

        elif method == 2:  # 根据 user_id 查找该用户评论了哪些书，以及评论内容和时间 (在create_time对book_id发表了评论)
            user_comment_records = db.session.query(UserComment, Books.title, Books.cover_image_url) \
                .join(Books, UserComment.book_id == Books.book_id) \
                .filter(UserComment.user_id == user_id) \
                .all()

            for user_comment, title, cover_image_url in user_comment_records:
                result.append({
                    'book_id': user_comment.book_id,
                    'title': title,
                    'cover_image_url': cover_image_url,
                    'content': user_comment.content,
                    'create_time': user_comment.create_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
                })

        elif method == 3:  # 根据 book_id 和 user_id 查找用户对特定书籍的评论 (在create_time发表了评论)
            user_comment = UserComment.query.filter_by(user_id=user_id, book_id=book_id).all()

            for comment_record in user_comment:
                result.append({
                    'content': comment_record.content,
                    'create_time': comment_record.create_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
                })

        else:  # 处理无效的 method 参数
            logger.error("无效的 method 参数: {}".format(method))

        return result

    def get_user_comment_record(self, method, book_id, user_id, current_page, page_size):
        result = []
        if method == 1:
            pass
        elif method == 2:
            user_comment_records = db.session.query(UserComment, Books.title, Books.cover_image_url) \
                .join(Books, UserComment.book_id == Books.book_id) \
                .filter(UserComment.user_id == user_id)

            # 按照收藏时间从新到旧的顺序进行排列
            user_comment_records = user_comment_records.order_by(desc(UserComment.create_time))
            # 进行分页处理，每页5个
            user_comment_records = user_comment_records.paginate(page=current_page, per_page=page_size, error_out=False)

            for user_comment, title, cover_image_url in user_comment_records:
                result.append({
                    'book_id': user_comment.book_id,
                    'title': title,
                    'cover_image_url': cover_image_url,
                    'content': user_comment.content,
                    'create_time': user_comment.create_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
                })
        return result

    def get_user_rating(self, method, user_id, book_id):
        # 构建结果字典列表
        result = []
        if method == 1:  # 根据 book_id 查找评分该书的用户、以及评分、时间 (user_id 在collect_time给本书评了rating)
            user_rating_records = db.session.query(UserRating, Users.username) \
                .join(Users, UserRating.user_id == Users.user_id) \
                .filter(UserRating.book_id == book_id) \
                .all()

            for user_rating, username in user_rating_records:
                result.append({
                    'user_id': user_rating.user_id,
                    'username': username,
                    'rating': user_rating.rating,
                    'rating_time': user_rating.rating_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
                })
        elif method == 2:  # 根据 user_id 查找该user评价了哪些书，评分 （在collect_time给book_id评了rating
            user_rating_records = db.session.query(UserRating, Books.title) \
                .join(Books, UserRating.book_id == Books.book_id) \
                .filter(UserRating.user_id == user_id) \
                .all()

            for user_rating, title in user_rating_records:
                result.append({
                    'book_id': user_rating.user_id,
                    'title': title,
                    'rating': user_rating.rating,
                    'rating_time': user_rating.rating_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
                })
        elif method == 3:  # 根据 book_id 和 user_id 查找收藏内容 (在collect_time,添加到了collect_type
            user_rating = UserRating.query.filter_by(user_id=user_id, book_id=book_id).all()
            for collect_record in user_rating:
                result.append({
                    'rating': collect_record.rating,
                    'rating_time': collect_record.rating_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
                })
        else:  # 处理无效的 method 参数
            logger.error("无效的 method 参数: {}".format(method))
        return result

    def get_user_rating_rocord(self, method, user_id, book_id, current_page, page_size):
        result = []
        if method == 1:
            pass
        elif method == 2:
            user_rating_records = db.session.query(UserRating, Books) \
                .join(Books, UserRating.book_id == Books.book_id) \
                .filter(UserRating.user_id == user_id)

            # 从新到旧排列
            user_rating_records = user_rating_records.order_by(desc(UserRating.rating_time))
            # 进行分页处理，每页5个
            user_rating_records = user_rating_records.paginate(page=current_page, per_page=page_size, error_out=False)

            for user_rating, book in user_rating_records:
                result.append({
                    'book_id': book.book_id,
                    'title': book.title,
                    'cover_image_url': book.cover_image_url,
                    'rating': user_rating.rating,
                    'rating_time': user_rating.rating_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
                })
        return result

    # 获取article_record
    def get_user_article_rocord(self, method, user_id, book_id, current_page, page_size):
        result = []
        # 根据book_id查找
        if method == 1:
            user_article_records = db.session.query(UserArticle, Users) \
                .join(Users, UserArticle.user_id == Users.user_id) \
                .filter(UserArticle.book_id == book_id)

            # 从新到旧排列
            user_article_records = user_article_records.order_by(desc(UserArticle.create_time))
            # 进行分页处理，每页5个
            user_article_records = user_article_records.paginate(page=current_page, per_page=page_size, error_out=False)

            for user_article, user in user_article_records:
                result.append({
                    'user_id': user.user_id,
                    'article_id' : user_article.article_id,
                    'article_title': user_article.article_title,
                    'avatar_path': user.avatar_path,
                    'create_time': user_article.create_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
                })
        # 根据user_id查找
        elif method == 2:
            user_article_records = db.session.query(UserArticle, Books) \
                .join(Books, UserArticle.book_id == Books.book_id) \
                .filter(UserArticle.user_id == user_id)

            # 从新到旧排列
            user_article_records = user_article_records.order_by(desc(UserArticle.create_time))
            # 进行分页处理，每页5个
            user_article_records = user_article_records.paginate(page=current_page, per_page=page_size, error_out=False)

            for user_article, book in user_article_records:
                result.append({
                    'book_id': book.book_id,
                    'title': book.title,
                    'article_title': user_article.article_title,
                    'cover_image_url': book.cover_image_url,
                    'create_time': user_article.create_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
                })
        return result

    # 获取article
    def get_article_by_article_id(self, article_id):
        article = UserArticle.query.filter_by(article_id=article_id).first()
        return article
