from operation.book import book_operation
from logger import create_logger
from utils.data_process import Data_Process

# logger
logger = create_logger(__name__)


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
#                    'publish_date','page_num','category','description','rating_num','comment_count'
# 需涉及到多表的联调,暂未实现
def get_detail_book_info(book_id):
    result = {}
    result['code'] = 0
    result['msg'] = "success"
    logger.info("get book detail info successfully ,book_id is {}".format(book_id))
    return result
