from models.users import bcrypt
from operation.user import user_operation
from logger import create_logger
from utils.data_process import Data_Process
import jwt
from db_config import app

# logger
logger = create_logger(__name__)


# 登录
def user_login(username, password):
    result = {}
    u = user_operation()
    data = u.get_user_by_username(username)
    if data is not None:
        if bcrypt.check_password_hash(data.password, password):  # True
            payload = {'user_id': data.user_id, 'username': data.username, 'password': password}
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            result['code'] = 0
            result['msg'] = "登录成功"
            result['token'] = token
            # data 数据处理
            result['user'] = Data_Process(data, u.detail_field, 1)
            logger.info("{} login successfully!".format(username))
        else:
            result['code'] = -1
            result['msg'] = "密码错误"
    else:
        result['code'] = -1
        result['msg'] = "username does not exit"
    return result


# 用户注册
def user_register(username, password, register_time):
    result = {}
    u = user_operation()
    data = u.get_user_by_username(username)
    if data is not None:
        result['code'] = -1  # 用户名重复，注册失败
        result['msg'] = "register fail, username already exits"
    elif password is None:
        result['code'] = -1  # 用户名重复，注册失败
        result['msg'] = "register fail, password must be non-empty"
    else:
        new_user = u.add_user(username, password, register_time)
        result['code'] = 0  # 注册成功
        result['msg'] = "register success"
        logger.info("{} register successfully!".format(username))
    return result


# 信息修改
def api_change_avatar(user_id, avatar_path):
    u = user_operation()
    result = u.change_avatar(user_id, avatar_path)
    return result


def api_change_password(user_id, password):
    u = user_operation()
    result = u.operation_change_password(user_id=user_id,password=password)
    return result


# avatar_path,username,register_time
def get_userinfo_by_user_id(user_id):
    result = {}
    u = user_operation()
    user = u.get_user_by_userid(user_id)
    if user is not None:
        # result['avatar_path'] = user.avatar_path
        # result['username'] = user.username
        # result['register_time'] = user.register_time
        result['code'] = 0  #
        result['user'] = Data_Process(user, u.basic_field, 1)
    else:
        result['code'] = -1
        result['msg'] = "fail to find required user"
    return result
