from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import config

app = Flask(__name__)
# 数据库类型 ip  port root  密码
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{config.DB_USER}:{config.DB_PWD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'
app.config['SECRET_KEY'] = 'spike_in_Bebop'

db_init = SQLAlchemy(app)