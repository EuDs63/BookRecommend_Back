from api.user import *
from flask import Blueprint, request
import json
from logger import create_logger
import os
import time
from utils.auth import token_required

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


@user.route('/auto_login', methods=['GET'])
@token_required
def auto_login(*args, **kwargs):
    user_data = kwargs.get('user_data')
    result = {}
    if user_data:
        # 如果 Token 验证成功，你可以在这里访问用户信息并执行相应操作
        user_id = user_data.get('user_id')
        username = user_data.get('username')
        password = user_data.get('password')
        logger.info("{} try to auto login!".format(username))
        # 调用api
        result = user_login(username, password)
    else:
        result['code'] = 0
        result['msg'] = 'Access denied'
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


# 根据user_id获取用户信息：avatar_path,username,register_time
@user.route('/<int:user_id>')
def getinfo(user_id):
    logger.info("try to get user info,user_id is {}".format(user_id))
    result = get_userinfo_by_user_id(user_id)
    return result


# 修改密码
@user.route('/update_password', methods=['POST'])
@token_required
def update_password(*args, **kwargs):
    result = {}
    # 获取user_data
    user_data = kwargs.get('user_data')

    if user_data is None:
        result['code'] = -1
        result['msg'] = '修改失败；登录状态已过期'
    else:
        # 解析token中的数据，获取user_data中所包含的信息
        user_id = user_data.get('user_id')
        password = user_data.get('password')

        # 解析post请求中的数据
        data = json.loads(request.data)
        origin_password = data['origin_password']
        new_password = data['new_password']

        # 检查传入的origin_password是否和实际上的password是否一致
        if origin_password == password:
            # 允许修改，调用api
            result['code'] = api_change_password(user_id=user_id, password=new_password)
            # 检查修改结果
            if result['code'] == 0:
                result['msg'] = "修改成功"
            else:
                result['msg'] = "修改失败"
        else:
            result['code'] = -1
            result['msg'] = '输入的原密码不正确'

    return result


# 上传头像
@user.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    result = {}
    # 获取上传的文件
    if 'avatar' not in request.files:
        result['code'] = -1
        result['msg'] = 'No avatar provided'
        logger.info("someone try to change avatar")
    else:
        # 获取POST数据
        avatar_file = request.files['avatar']
        user_id = request.form['user_id']
        logger.info("{} try to change avatar".format(user_id))
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
