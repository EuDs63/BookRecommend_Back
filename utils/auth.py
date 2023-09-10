import datetime

import jwt
from flask import request, jsonify
from db_config import app
from logger import create_logger
from functools import wraps
logger = create_logger(__name__)

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        result = {}
        if not token:
            result['msg'] = 'Token is missing'
            result['code'] = -1
            return result

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            result['msg'] = 'Token has expired'
            result['code'] = -1
            return result
        except jwt.InvalidTokenError:
            result['msg'] = 'Token is missing'
            result['code'] = -1
            return result

        # 在此可以将用户信息从 token 中提取，并将其传递给路由
        kwargs['user_data'] = data

        return f(*args, **kwargs)

    return wrapper


# 用户登录成功后生成 JWT，并设置过期时间为一小时
def generate_token(user_id, username,password):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'user_id': user_id,
        'username': username,
        'password': password,
        'exp': expiration_time  # 设置过期时间
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token
