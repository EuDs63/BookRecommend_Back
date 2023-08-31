from operation.user import user_operation
from operation.admin import admin_operation
from logger import create_logger
from utils.data_process import Data_Process

# logger
logger = create_logger(__name__)


# 管理员注册
def admin_register(username, password, register_time):
    result = {}
    # 通过user_operation查询数据库中是否存在同名yonghu
    u = user_operation()
    data = u.getUserByUsername(username)
    if data is not None:
        result['code'] = -1  # 用户名重复，注册失败
        result['msg'] = "register fail, username already exits"
    else:
        # 无同名用户，允许注册
        a = admin_operation()  # 使用admin_operation操作数据库
        new_user = a.addAdmin(username, password, register_time)
        result['code'] = 0  # 注册成功
        result['msg'] = "register to be an admin success"
        logger.info("{} register to be an admin successfully!".format(username))
    return result


# 获取所有用户的信息
def admin_getAllUsers():
    result = {}
    u = user_operation()
    a = admin_operation()
    data = a.getAllUser()
    if data is None:
        result['code'] = -1  # 失败
        result['msg'] = "get all users fail"
    else:
        result['code'] = 0  # 成功
        result['users'] = Data_Process(data, u.fields, 0)
    return result
