from api.user import *
from flask import Blueprint, request
import json
from logger import create_logger

logger = create_logger(__name__)
# 第1步
user = Blueprint('user', __name__)


# 第3步
@user.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    # 获取数据
    username = data['username']
    password = data['password']
    logger.info("{} try to login!".format(username))
    # 调用api
    result = user_login(username, password)
    return result


@user.route('/register',methods=['POST'])
def register():
    data = json.loads(request.data)
    # 获取数据
    username = data['username']
    password = data['password']
    register_time = data['register_time']
    logger.info("{} try to register!".format(username))
    # 调用api
    result = user_register(username, password,register_time)
    return result


@user.route('/changeinfo')
def changeinfo():
    return "changeinfo"


@user.route('/getinfo')
def getinfo():
    return "getinfo"
