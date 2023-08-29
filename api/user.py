from operation.user import user_operation
from flask import jsonify
from logger import create_logger

logger = create_logger(__name__)


def user_login(username, password):
    u = user_operation()
    # 获取user
    user = u.login(username, password)
    code = 0
    # 验证
    if user.password == password:
        code = 0
        logger.info("{} login successfully!".format(username))
    else:
        code = -1
    return jsonify(code)
