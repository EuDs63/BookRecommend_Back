from flask import Blueprint, request
import json
from logger import create_logger
from api.action import *

logger = create_logger(__name__)

action = Blueprint('action', __name__)


# action： 包含user_collect,user_comment,user_rating三类
# 合并原因: 三者操作有一定的相似性

@action.route('/add', methods=['POST'])
def add():
    data = json.loads(request.data)
    type = data['type']
    user_id = data['user_id']
    book_id = data['book_id']
    content = data['content']
    # 根据type来区分不同的action:
    # 1：collect; 2：comment 3: rating
    logger.info("user {} try to add action , type is {}".format(user_id,type))
    result = api_add_action(type, user_id, book_id, content)
    return result
