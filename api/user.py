from operation.user import user_operation
from flask import jsonify
from logger import create_logger
from utils.data_process import Data_Process

# logger
logger = create_logger(__name__)


# 登录
def user_login(username, password):
    result = {}
    u = user_operation()
    data = u.getUserByUsername(username)
    if data is not None:
        if data.password == password:
            result['code'] = 0
            result['msg'] = "login success"
            # data 数据处理
            result['user'] = Data_Process(data, u.fields, 1)
        else:
            result['code'] = -1
            result['msg'] = "err password"
    else:
        result['code'] = -1
        result['msg'] = "username does not exit"
    return result
