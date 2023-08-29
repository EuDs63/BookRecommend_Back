from api.user import *
from flask import Blueprint, request
import json

# 第1步
user = Blueprint('user', __name__)


# 第3步
@user.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    # 获取数据
    username = data['username']
    password = data['password']
    # 调用api
    result = user_login(username, password)
    return result


@user.route('/register')
def register():
    return "register"


@user.route('/changeinfo')
def changeinfo():
    return "changeinfo"


@user.route('/getinfo')
def getinfo():
    return "getinfo"
