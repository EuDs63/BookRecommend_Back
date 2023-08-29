from operation.user import user_operation
from flask import jsonify


def user_login(username, password):
    u = user_operation()
    # 获取user
    user = u.login(username, password)
    code = 0
    # 验证
    if user.password == password:
        code = 0
    else:
        code = -1
    return jsonify(code)
