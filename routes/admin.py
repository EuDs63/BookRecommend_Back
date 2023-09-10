from api.user import user_login
from api.admin import *
from flask import Blueprint, request
from logger import create_logger
import json

logger = create_logger(__name__)

admin = Blueprint('admin', __name__)


# 管理员登录
@admin.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    # 获取数据
    username = data['username']
    password = data['password']
    logger.info("admin {} try to login!".format(username))
    # 调用api
    result = user_login(username, password)
    return result

# 获取全部用户信息
@admin.route('/getAllUsers',methods=['GET'])
def getAllUsers():
    logger.info("try to return all user information")
    # 调用api
    result = admin_getAllUsers()
    return result


# 管理员注册:区别仅在于is_admin
@admin.route('/register', methods=['POST'])
def register():
    data = json.loads(request.data)
    # 获取数据
    username = data['username']
    password = data['password']
    register_time = data['register_time']
    logger.info("{} try to register to be an admin!".format(username))
    # 调用api
    result = admin_register(username, password, register_time)
    return result
