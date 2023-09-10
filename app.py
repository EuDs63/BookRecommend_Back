from flask import Flask, Blueprint
from routes.user import user
from routes.admin import admin
from routes.book import book
from routes.action import action
from db_config import app
from flask_cors import CORS

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(book, url_prefix='/book')
app.register_blueprint(action, url_prefix='/action')
CORS(app)


@app.route('/')
def ping():
    return "OK"


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
