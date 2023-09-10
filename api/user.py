from models.user import bcrypt
from operation.user import user_operation
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
        if bcrypt.check_password_hash(data.password, password):  # True
            result['code'] = 0
            result['msg'] = "login success"
            # data 数据处理
            result['user'] = Data_Process(data, u.fields, 1)
            logger.info("{} login successfully!".format(username))
        else:
            result['code'] = -1
            result['msg'] = "err password"
    else:
        result['code'] = -1
        result['msg'] = "username does not exit"
    return result


# 用户注册
def user_register(username, password, register_time):
    result = {}
    u = user_operation()
    data = u.getUserByUsername(username)
    if data is not None:
        result['code'] = -1  # 用户名重复，注册失败
        result['msg'] = "register fail, username already exits"
    else:
        new_user = u.addUser(username, password, register_time)
        result['code'] = 0  # 注册成功
        result['msg'] = "register success"
        logger.info("{} register successfully!".format(username))
    return result



