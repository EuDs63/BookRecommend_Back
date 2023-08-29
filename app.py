from flask import Flask,Blueprint
from routes.user import user

# app = Flask(__name__
from db_config import app

# 第2步 注册模块user
app.register_blueprint(user, url_prefix='/user')



@app.route('/')
def ping():
    return "OK"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
