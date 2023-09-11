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
    # 根据type来区分不同的action:
    # 1：collect; 2：comment 3: rating
    logger.info("user {} try to add action , type is {}".format(user_id, type))
    result = api_add_action(type, user_id, book_id, content)
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
    logger.info("try to get collect ,method is {},book_id is {}, user_id is {} ".format(method, book_id, user_id))
    result = api_get_collect(method, book_id, user_id, current_page)
    return result


# 获取rating
@action.route('/rating/<int:method>/<int:book_id>/<int:user_id>')
def get_rating(method, book_id, user_id):
    current_page = int(request.args.get('current_page', 1))
    logger.info(
        "try to get rating,method is {},book_id is {}, user_id is {},current_page is {} ".format(method, book_id,
                                                                                                 user_id, current_page))
    result = api_get_action(3, method, book_id, user_id, current_page)
    return result

# 获取comment
@action.route('/comment/<int:method>/<int:book_id>/<int:user_id>')
def get_comment(method, book_id, user_id):
    current_page = int(request.args.get('current_page', 1))
    logger.info(
        "try to get comment,method is {},book_id is {}, user_id is {},current_page is {} ".format(method, book_id,
                                                                                                  user_id, current_page))
    result = api_get_comment(method, book_id, user_id, current_page)
    return result