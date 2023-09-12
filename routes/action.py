from flask import Blueprint, request
import json
from logger import create_logger
from api.action import *

logger = create_logger(__name__)

action = Blueprint('action', __name__)


# action： 包含user_collect,user_comment,user_rating三类
# 合并原因: 三者操作有一定的相似性

@action.route('/add', methods=['POST'])
def add_action():
    data = json.loads(request.data)
    type = data['type']
    user_id = data['user_id']
    book_id = data['book_id']
    content = data['content']
    # 检查是否存在 article_title，如果不存在则设置为默认值 null
    if 'article_title' not in data:
        article_title = None
    else:
        article_title = data['article_title']
    # 根据type来区分不同的action:
    # 1：collect; 2：comment 3: rating 4: article
    logger.info("user {} try to add action , type is {}".format(user_id, type))
    result = api_add_action(type, user_id, book_id, content,article_title)
    return result


@action.route('/get', methods=['POST'])
def get_action():
    data = json.loads(request.data)
    type = data['type']  # 内容类型
    method = data['method']  # 获取方式
    book_id = data.get('book_id', 0)
    user_id = data.get('user_id', 0)  # 如果找不到 'user_id' 键，user_id 将被设置为 0
    current_page = data.get('current_page', 0)
    # 根据 type 和 method 获取相应的内容
    logger.info("Try to get content, type: {}, method: {},user_id: {}".format(type, method, user_id))
    result = api_get_action(type, method, book_id, user_id, current_page)
    return result


# 获取collect
@action.route('/collect/<int:method>/<int:book_id>/<int:user_id>')
def get_collect(method, book_id, user_id):
    current_page = int(request.args.get('current_page', 1))
    page_size = int(request.args.get('page_size', 3))

    logger.info("try to get collect ,method is {},book_id is {}, user_id is {} ".format(method, book_id, user_id))
    result = api_get_collect(method, book_id, user_id, current_page, page_size)
    return result


# 获取rating
@action.route('/rating/<int:method>/<int:book_id>/<int:user_id>')
def get_rating(method, book_id, user_id):
    current_page = int(request.args.get('current_page', 1))
    page_size = int(request.args.get('page_size', 3))
    logger.info(
        "try to get rating,method is {},book_id is {}, user_id is {},current_page is {} ".format(method, book_id,
                                                                                                 user_id, current_page))
    if method == 2:
        result = api_get_rating_record(method, book_id, user_id, current_page, page_size=page_size)
    else:
        result = api_get_action(3, method, book_id, user_id, current_page)
    return result


# 获取comment
@action.route('/comment/<int:method>/<int:book_id>/<int:user_id>')
def get_comment(method, book_id, user_id):
    current_page = int(request.args.get('current_page', 1))
    page_size = int(request.args.get('page_size', 3))
    logger.info(
        "try to get comment,method is {},book_id is {}, user_id is {},current_page is {} ".format(method, book_id,
                                                                                                  user_id,
                                                                                                  current_page))
    result = api_get_comment_record(method, book_id, user_id, current_page, page_size)
    return result


# 获取article
@action.route('/article/<int:method>/<int:book_id>/<int:user_id>')
def get_article_record(method, book_id, user_id):
    current_page = int(request.args.get('current_page', 1))
    page_size = int(request.args.get('page_size', 3))
    logger.info(
        "try to get article record,method is {},book_id is {}, user_id is {},current_page is {} ".format(method, book_id,
                                                                                                  user_id,
                                                                                                  current_page))
    result = api_get_article_record(method, book_id, user_id, current_page, page_size)
    return result

@action.route('/article/view/<int:article_id>')
def get_article(article_id):
    logger.info('try to get article by article_id'.format(article_id))
    result = api_get_article(article_id)
    return result


