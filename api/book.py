from operation.book import book_operation
from logger import create_logger
from utils.data_process import Data_Process, Paginate_Process

# logger
logger = create_logger(__name__)


def api_load_books():
    b = book_operation()
    json_file_path = 'D:\BookRecommend\BookRecommend_Back\static\douban_09-04_14-15.json'
    count = b.load_books_to_database(json_file_path)
    books_count = count[0]
    success_count = count[1]
    result = {}
    result['code'] = 0
    result['msg'] = "计划导入{}本书,成功导入{}本书到数据库".format(books_count, success_count)
    return result


# recommendedBooksData： 'book_id','author','cover_image_url','title','rating_avg','description'
def get_basic_book_info(book_id):
    result = {}
    b = book_operation()
    data = b.getBookById(book_id)
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
# 需涉及到多表的联调,暂未实现
def get_detail_book_info(book_id):
    result = {}
    b = book_operation()
    data = b.getBookById(book_id)
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
def api_get_category_book(category_id, current_page, per_page):
    b = book_operation()
    # 对所有书籍信息进行分页查询
    books_pagination = b.return_category_book_infos(category_id, current_page, per_page)
    # 对得到的分页查询进行处理
    result = Paginate_Process(books_pagination, current_page, b.basic_field)
    result['category_id'] = category_id
    return result

# 分页返回特定tag的所有书籍基本信息
def api_get_tag_book(tag_id, current_page, per_page):
    b = book_operation()
    # 对所有书籍信息进行分页查询
    books_pagination = b.return_tag_book_infos(tag_id, current_page, per_page)
    # 对得到的分页查询进行处理
    result = Paginate_Process(books_pagination, current_page, b.basic_field)
    result['tag_id'] = tag_id
    return result
