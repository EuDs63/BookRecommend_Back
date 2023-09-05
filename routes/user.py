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
    return "changeinfo"


# 根据user_id获取用户信息：avatar_path,username,register_time
@user.route('/<int:user_id>')
def getinfo(user_id):
    logger.info("try to get user info,user_id is {}".format(user_id))
    result = get_userinfo_by_user_id(user_id)
    return result


# 上传头像
@user.route('/upload-avatar', methods=['POST'])
def upload_avatar():
    result = {}
    # 获取上传的文件
    if 'avatar' not in request.files:
        result['code'] = -1
        result['msg'] = 'No avatar provided'
    else:
        # 获取POST数据
        avatar_file = request.files['avatar']
        user_id = request.form['user_id']
        # 生成文件名
        timestamp = int(time.time())  # 当前时间的时间戳
        filename_without_extension, file_extension = os.path.splitext(avatar_file.filename)
        save_filename = f"user_{user_id}_{timestamp}{file_extension}"
        save_path = 'static/avatar/' + save_filename

        # 调用api,以更新数据库中对应user的avatar_path
        result['code'] = api_change_avatar(user_id, save_path)
        if result['code'] == 0:
            result['avatar_path'] = save_path
            # 保存文件
            avatar_file.save(save_path)
        else:
            result['msg'] = 'No such user'

    return result
