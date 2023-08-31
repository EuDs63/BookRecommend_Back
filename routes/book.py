from flask import Blueprint, request
import json
from logger import create_logger
from db_config import db_init as db
from models.books import Books
logger = create_logger(__name__)

book = Blueprint('book', __name__)


@book.route('/insert_books', methods=['GET'])
def insert_books():
    # 打开文本文件并逐行处理
    with open('books.txt', 'r', encoding='utf-8') as file:
        for line in file:
            fields = line.strip().split(',')
            title = fields[0]
            rating_avg = float(fields[1])
            comment_count = int(fields[2])
            author = fields[3].split(': ')[1]
            publisher = fields[4]
            publish_date = datetime.strptime(fields[5], '%Y-%m')
            cover_image_url = fields[6]

            # 创建 Books 实例并插入到数据库
            book = Books(
                title=title,
                rating_avg=rating_avg,
                comment_count=comment_count,
                author=author,
                publisher=publisher,
                publish_date=publish_date,
                cover_image_url=cover_image_url,
                description='',  # 这里可以添加适当的描述
            )
            db.session.add(book)
            db.session.commit()

    print("插入完成")
