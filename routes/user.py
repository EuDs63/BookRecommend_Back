from api.user import *
from flask import Blueprint, request
import json
from logger import create_logger
import os
import time

logger = create_logger(__name__)

user = Blueprint('user', __name__)


# 用户登录
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


# 用户注册
@user.route('/register', methods=['POST'])
def register():
    data = json.loads(request.data)
    # 获取数据
    username = data['username']
    password = data['password']
    register_time = data['register_time']
    logger.info("{} try to register!".format(username))
    # 调用api
    result = user_register(username, password, register_time)
    return result


@user.route('/changeinfo')
def changeinfo():
    # 用户信息修改应实现这样的操作：将各种信息修改合在一个函数中
    return "changeinfo"


@user.route('/getinfo')
def getinfo():
    return "getinfo"


@user.route('/upload-avatar', methods=['POST'])
def upload_avatar():
    result = {}
    # 获取上传的文件
    if 'avatar' not in request.files:
        result['code'] = -1
        result['msg'] = 'No avatar provided'
        return result
    else:
        # 获取POST数据
        avatar_file = request.files['avatar']
        user_id = request.form['user_id']
        # 生成文件名
        timestamp = int(time.time())  # 当前时间的时间戳
        filename_without_extension, file_extension = os.path.splitext(avatar_file.filename)
        save_filename = f"user_{user_id}_{timestamp}{file_extension}"
        # 保存文件
        avatar_file.save('static/avatar/' + save_filename)
        # 调用api,以更新数据库中对应user的avatar_path



