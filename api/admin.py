from models.user import bcrypt
from operation.user import user_operation
from logger import create_logger
from utils.data_process import Data_Process

# logger
logger = create_logger(__name__)


# 管理员注册
def admin_register(username, password, register_time):
    result = {}
    u = user_operation()
    data = u.getUserByUsername(username)
    if data is not None:
        result['code'] = -1  # 用户名重复，注册失败
        result['msg'] = "register fail, username already exits"
    else:
        new_user = u.addAdmin(username, password, register_time)
        result['code'] = 0  # 注册成功
        result['msg'] = "register to be an admin success"
        logger.info("{} register to be an admin successfully!".format(username))
    return result
