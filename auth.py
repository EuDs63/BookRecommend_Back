import jwt
from flask import request, jsonify
from db_config import app


def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        # 在此可以将用户信息从 token 中提取，并将其传递给路由
        kwargs['user_data'] = data

        return f(*args, **kwargs)

    return wrapper
