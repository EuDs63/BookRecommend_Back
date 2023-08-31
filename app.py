from flask import Flask, Blueprint
from routes.user import user
from routes.admin import admin
from db_config import app
from flask_cors import CORS

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(admin, url_prefix='/admin')
CORS(app)


@app.route('/')
def ping():
    return "OK"


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
