from flask import Blueprint, request
import json
from logger import create_logger
from db_config import db_init as db
from models.books import Books
from api.book import *
import os
import time

logger = create_logger(__name__)

book = Blueprint('book', __name__)


# 读取douban.txt中的信息，并加载到数据库中
# @book.route('/insert_books', methods=['GET'])
# def insert_books():
#     # 打开文本文件并逐行处理
#     with open('D:\BookRecommend\BookRecommend_Back\static\douban.txt', 'r', encoding='utf-8') as file:
#         for line in file:
#             fields = line.strip().split(',')
#             title = fields[0]
#             rating_avg = float(fields[1])
#             rating_num = int(fields[2])
#             author = fields[3].split(': ')[1]
#             publisher = fields[4]
#             publish_date = fields[5]
#             cover_image_url = fields[6]
#
#             # 创建 Books 实例并插入到数据库
#             book = Books(
#                 isbn='',
#                 title=title,
#                 rating_avg=rating_avg,
#                 comment_count=0,
#                 author=author,
#                 publisher=publisher,
#                 page_num=0,
#                 publish_date=publish_date,
#                 cover_image_url=cover_image_url,
#                 rating_num=rating_num,
#                 description='',  # 这里可以添加适当的描述
#             )
#             db.session.add(book)
#             db.session.commit()
#
#     print("插入完成")
#     return ("数据库更新成功")


# 读取douban.json中的信息，并加载到数据库中
# 这个过程应包含四个表的更新:books,book_categories,tags,book_tags
@book.route('/load_books', methods=['GET'])
def load_books():
    logger.info("try to load books to database")
    json_file_path = 'D:\BookRecommend\BookRecommend_Back\static\book\douban_09-04_14-15.json'
    result = api_load_books(json_file_path)
    return result


# 插入一条书的数据到数据库中
@book.route('insert_book', methods=['POST'])
def insert_book():
    book_info = json.loads(request.data)
    logger.info("try to insert book to database")
    result = api_insert_book(book_info)
    return result


# 根据id获取图书信息 根据前端需求的不同，所返回的图书信息包含的内容也应不同
# type 类型:
# 0 recommendedBooksData： 'book_id','author','cover_image_url','title','rating_avg','description'
# 1 bookDetailsData : 'book_id','isbn','cover_image_url','title','author','publisher','rating_avg',
#                     'publish_date','page_num','category','description','rating_num','comment_count'
@book.route('/<int:book_id>/<int:info_type>')
def get_book_info(book_id, info_type):
    logger.info("try to get book info,book_id is {}, type is {} ".format(book_id, info_type))
    result = {}
    if info_type == 0:
        result = get_basic_book_info(book_id)
    elif info_type == 1:
        result = get_detail_book_info(book_id)
    else:
        result['code'] = -1  # 暂无相关需求
        result['msg'] = "unsupported info_type"
    return result


# 上传书籍信息文件
@book.route('/upload_books', methods=['POST'])
def upload_book():
    result = {}
    # 获取上传的文件
    if 'books' not in request.files:
        result['code'] = -1
        result['msg'] = 'No books provided'
    else:
        # 获取POST数据
        book_file = request.files['books']
        # 生成文件名
        timestamp = int(time.time())  # 当前时间的时间戳
        filename_without_extension, file_extension = os.path.splitext(book_file.filename)
        save_filename = f"books_{timestamp}{file_extension}"
        save_path = 'static/book/' + save_filename
        # 保存文件
        book_file.save(save_path)
        # 调用api
        result = api_load_books(json_file_path=save_path)
    return result


@book.route('/all', methods=['GET'])
def get_all_books():
    page = request.args.get('page', 1, type=int)  # 所要查询的页号，默认值为1
    per_page = request.args.get('per_page', 20, type=int)  # 每页显示的书籍数量,默认值为20
    logger.info("try to get all book info,current page is {} ".format(page))
    result = api_get_all_books(page, per_page)
    return result


# 根据category_id分页返回该类下所有的书籍信息
# 根据order来区分： 0：默认；1：日期由新到旧；2：rating_num从多到少
@book.route('/category', methods=['GET'])
def get_category_books():
    category_id = request.args.get('category_id', 1, type=int)
    page = request.args.get('page', 1, type=int)  # 所要查询的页号，默认值为1
    per_page = request.args.get('per_page', 20, type=int)  # 每页显示的书籍数量,默认值为20
    order = request.args.get('order', 0, type=int)  # 显示书籍的顺序
    logger.info("try to get book info which category_id is {},current page is {} ".format(category_id, page))
    result = api_get_category_book(category_id, page, per_page, order)
    return result


# 根据tag_id分页返回该类下所有的书籍信息
@book.route('/tag', methods=['GET'])
def get_tag_books():
    # 获取参数
    tag_id = request.args.get('tag_id', 1, type=int)
    page = request.args.get('page', 1, type=int)  # 所要查询的页号，默认值为1
    per_page = request.args.get('per_page', 20, type=int)  # 每页显示的书籍数量,默认值为20
    logger.info("try to get book info which tag_id is {}, current page is {} ".format(tag_id, page))
    # 调用api
    result = api_get_tag_book(tag_id, page, per_page)
    return result


# 实现搜索功能
@book.route('/search', methods=['GET'])
def search():
    # 获取用户输入的搜索关键字
    keyword = request.args.get('keyword', '')
    page = request.args.get('page', 1, type=int)  # 所要查询的页号，默认值为1
    per_page = request.args.get('per_page', 20, type=int)  # 每页显示的书籍数量,默认值为20
    method = request.args.get('method', 1, type=int)  # 搜索方法：默认为1（对标题、作者）进行模糊搜索
    logger.info("try to search book info which keyword is {}, current page is {} ".format(keyword, page))
    # 调用api
    result = api_get_searched_book(keyword, page, per_page, method)
    return result


@book.route('/edit', methods=['POST'])
def edit():
    data = json.loads(request.data)
    # 获取数据
    book_id = data['book_id']
    edit_info = data['edit_info']
    result = api_edit_info(book_id, edit_info)
    return result


@book.route('/train', methods=['POST'])
def train():
    result = api_train()
    return result

# 根据user_id获得相关推荐
@book.route('/getrec/<int:user_id>', methods=['GET'])
def getrec(user_id):
    result = api_get_recommend(user_id)
    return result

# 根据book_id获得相关推荐
@book.route('/recommendationByBookId/<int:book_id>',methods=['GET'])
def recommendation_by_book_id(book_id):
    logger.info('try to get recommended book by book_id');
    result = api_recommendation_by_book_id(book_id)
    return result
