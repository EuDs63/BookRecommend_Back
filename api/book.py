import random

from operation.book import book_operation
from operation.action import action_operation
from logger import create_logger
from utils.data_process import Data_Process, Paginate_Process

# logger
logger = create_logger(__name__)


def api_load_books(json_file_path):
    b = book_operation()
    count = b.load_books_to_database(json_file_path)
    books_count = count[0]
    success_count = count[1]
    result = {}
    result['code'] = 0
    result['msg'] = "计划导入{}本书,成功导入{}本书到数据库".format(books_count, success_count)
    return result


def api_insert_book(book_info):
    result = {}
    b = book_operation()
    result['book_id'] = b.insert_book_to_database(book_info)
    if result['book_id'] == 0:
        result['code'] = -1
        result['msg'] = "添加书籍信息失败"
    else:
        result['code'] = 0
        result['msg'] = "添加书籍信息成功"
    return result


# recommendedBooksData： 'book_id','author','cover_image_url','title','rating_avg','description'
def get_basic_book_info(book_id):
    result = {}
    b = book_operation()
    data = b.get_book_by_id(book_id)
    if data is not None:
        result['book'] = Data_Process(data, b.basic_field, 1)
        result['code'] = 0  # 获取成功
        result['msg'] = "success"
        logger.info("get book basic info successfully ,book_id is {}".format(book_id))
    else:
        result['code'] = -1  # 获取失败
        result['msg'] = "can not find such book"
        logger.info("fail to get book basic info ,book_id is {}".format(book_id))
    return result


# bookDetailsData : 'book_id','isbn','cover_image_url','title','author','publisher','rating_avg',
#                    'publish_date','page_num','description','rating_num','comment_count','category','tag'
# 需涉及到多表的联调,已实现
def get_detail_book_info(book_id):
    result = {}
    b = book_operation()
    data = b.get_book_by_id(book_id)
    if data is not None:
        book = Data_Process(data, b.detail_field, 1)
        category = b.get_category_by_book_id(book_id)
        tag = b.get_tags_by_book_id(book_id)
        book["category"] = category
        book["tag"] = tag
        result['book'] = book
        result['code'] = 0
        result['msg'] = "success"
        logger.info("get book detail info successfully ,book_id is {}".format(book_id))
    else:
        result['code'] = -1  # 获取失败
        result['msg'] = "can not find such book"
        logger.info("fail to get book detail info ,book_id is {}".format(book_id))
    return result


# 分页返回所有书籍信息
def api_get_all_books(current_page, per_page):
    b = book_operation()
    # 对所有书籍信息进行分页查询
    books_pagination = b.return_all_book_infos(current_page, per_page)
    # 对得到的分页查询进行处理
    result = Paginate_Process(books_pagination, current_page, b.detail_field)
    return result


# 分页返回特定category的所有书籍基本信息
def api_get_category_book(category_id, current_page, per_page, order):
    b = book_operation()
    # 进行分页查询
    books_pagination = b.return_category_book_infos(category_id, current_page, per_page, order)
    # 对得到的分页查询进行处理
    result = Paginate_Process(books_pagination, current_page, b.basic_field)
    result['category_id'] = category_id
    result['order'] = order
    return result


# 分页返回特定tag的所有书籍基本信息
def api_get_tag_book(tag_id, current_page, per_page):
    b = book_operation()
    # 进行分页查询
    books_pagination = b.return_tag_book_infos(tag_id, current_page, per_page)
    # 对得到的分页查询进行处理
    result = Paginate_Process(books_pagination, current_page, b.search_field)
    result['tag_id'] = tag_id
    return result


def api_get_searched_book(keyword, current_page, per_page, method):
    b = book_operation()
    result = {}
    # 进行分页查询
    books_pagination = b.return_searched_book_infos(keyword, current_page, per_page, method)
    if books_pagination is not None:
        # 对得到的分页查询进行处理
        result = Paginate_Process(books_pagination, current_page, b.search_field)
    else:
        result['code'] = -1
        result['msg'] = "search fail"
    return result


def api_edit_info(book_id, edit_info):
    result = {}
    b = book_operation()
    if b.edit_info(book_id, edit_info) == 0:
        result['code'] = 0
        result['msg'] = "success"
    else:
        result['code'] = -1
        result['msg'] = "fail"
    return result


# 训练
def api_train():
    result = {}
    b = book_operation()
    if b.ItemSimilarity() != 0:
        result['code'] = 0
        result['msg'] = "success"
    else:
        result['code'] = -1
        result['msg'] = "fail"
    return result


# 获得推荐
def api_get_recommend(user_id):
    result = {}
    b = book_operation()
    book_data = b.Recommendation(user_id)
    result['books'] = []
    if book_data != 0:
        result['book_id'] = list(book_data.keys())
        # 已有的book_id
        existing_book_ids = result['book_id']
        # 生成随机数字，确保不重复
        def generate_random_numbers(existing_numbers, n):
            random_numbers = set()
            while len(random_numbers) < n:
                new_number = random.randint(1, 8)
                if new_number not in existing_numbers and new_number not in random_numbers:
                    random_numbers.add(new_number)
            return list(random_numbers)
        # 检查需要生成的数量
        remaining_count = 5 - len(existing_book_ids)
        if remaining_count > 0:
            random_numbers = generate_random_numbers(existing_book_ids, remaining_count)
            result['book_id'].extend(random_numbers)
        for book_id in list(result['book_id']):
            data = b.get_book_by_id(book_id)
            book = Data_Process(data, b.detail_field, 1)
            result["books"].append(book)
        result['code'] = 0
        result['msg'] = "success"
    else:
        result['code'] = -1
        result['msg'] = "fail"
    return result


def generate_random_values_around(target_integer, num_values, range_size):
    values = []

    for _ in range(num_values):
        while True:
            value = random.randint(target_integer - range_size, target_integer + range_size)
            if 1 <= value <= 1900 and value != target_integer:
                values.append(value)
                break

    return values


# 根据book_id获得相关推荐
def api_recommendation_by_book_id(book_id):
    values = generate_random_values_around(book_id, 6, 20)
    b = book_operation()
    a = action_operation()
    result = []
    for value in values:
        book = b.get_book_by_id(value)
        book_info = Data_Process(book, b.basic_field, 1)
        members = a.get_collect_members(book.book_id)
        book_info["members"] = members
        result.append(book_info)
    return result
