from flask import Blueprint, request
import json
from logger import create_logger
from db_config import db_init as db
from models.book import Books
from api.book import *

logger = create_logger(__name__)

book = Blueprint('book', __name__)


@book.route('/insert_books', methods=['GET'])
def insert_books():
    # 打开文本文件并逐行处理
    with open('D:\BookRecommend\BookRecommend_Back\static\douban.txt', 'r', encoding='utf-8') as file:
        for line in file:
            fields = line.strip().split(',')
            title = fields[0]
            rating_avg = float(fields[1])
            rating_num = int(fields[2])
            author = fields[3].split(': ')[1]
            publisher = fields[4]
            publish_date = fields[5]
            cover_image_url = fields[6]

            # 创建 Books 实例并插入到数据库
            book = Books(
                isbn='',
                title=title,
                rating_avg=rating_avg,
                comment_count=0,
                author=author,
                publisher=publisher,
                page_num=0,
                publish_date=publish_date,
                cover_image_url=cover_image_url,
                rating_num=rating_num,
                description='',  # 这里可以添加适当的描述
            )
            db.session.add(book)
            db.session.commit()

    print("插入完成")
    return ("数据库更新成功")


# 根据id获取图书信息 根据前端需求的不同，所返回的图书信息包含的内容也应不同
# type 类型:
# 0 recommendedBooksData： 'book_id','author','cover_image_url','title','rating_avg','description'
# 1 bookDetailsData : 'book_id','isbn','cover_image_url','title','author','publisher','rating_avg',
#                     'publish_date','page_num','category','description','rating_num','comment_count'
@book.route('/<int:book_id>/<int:info_type>')
def get_book_info(book_id, info_type):
    logger.info("try to get book info,book_id is {}, type is {} ".format(book_id, info_type))
    result = {}
    if info_type == 0:
        result = get_basic_book_info(book_id)
    elif info_type == 1:
        result = get_detail_book_info(book_id)
    else:
        result['code'] = -1  # 暂无相关需求
        result['msg'] = "unsupported info_type"
    return result
