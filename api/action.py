from operation.action import action_operation
from logger import create_logger
from db_config import db_init as db
from utils.data_process import Data_Process, Paginate_Process

# logger
logger = create_logger(__name__)


def api_add_action(type, user_id, book_id, content):
    result = {}
    a = action_operation()
    # 根据type来区分不同的action:
    # 1：collect; 2：comment 3: rating
    if type == 1:
        a.add_user_collect(user_id, book_id, content)
    elif type == 2:
        a.add_user_comment(user_id, book_id, content)
    elif type == 3:
        a.add_user_rating(user_id, book_id, content)
    elif type == 4:
        a.add_user_article(user_id, book_id, content)
    else:
        result["code"] = -1
        result["msg"] = "不支持的action type"
    try:
        db.session.commit()
        result["code"] = 0
        result["msg"] = "success"
    except Exception as e:
        db.session.rollback()  # 回滚事务，取消数据库更改
        logger.error(f"添加数据时发生异常: {e}")
        result["code"] = -1
        result["msg"] = f"add action fail,the reason is {e}"
    return result


def api_get_action(type, method, book_id, user_id, current_page):
    result = {}
    a = action_operation()
    # 根据type来区分不同的action:
    # 1：collect; 2：comment 3: rating
    if type == 1:  # collect
        result["content"] = a.get_user_collect(method=method, user_id=user_id, book_id=book_id,
                                               current_page=current_page)
        result["code"] = 0
    elif type == 2:  # comment
        result["content"] = a.get_user_comment(method=method, user_id=user_id, book_id=book_id)
        result["code"] = 0
    elif type == 3:  # rating
        result["content"] = a.get_user_rating(method=method, user_id=user_id, book_id=book_id)
        result["code"] = 0
    else:
        result["code"] = -1
        result["msg"] = "不支持的action type"

    return result


def api_get_collect(method, book_id, user_id, current_page, page_size):
    a = action_operation()
    if method == 2:  # 先这样凑合着
        result = a.get_user_collect_records(method=method, user_id=user_id, book_id=book_id, current_page=current_page,
                                            page_size=page_size)
    else:
        result = a.get_user_collect(method=method, user_id=user_id, book_id=book_id, current_page=current_page)
    return result


# def api_get_rating(method, book_id, user_id, current_page):
#     a = action_operation()
#     result = a.get_user_collect(method=method, user_id=user_id, book_id=book_id, current_page=current_page)
#     return result

def api_get_comment_record(method, book_id, user_id, current_page, page_size):
    a = action_operation()
    result = a.get_user_comment_record(method=method, user_id=user_id, book_id=book_id, current_page=current_page,
                                       page_size=page_size)
    return result


# 获取评分记录
def api_get_rating_record(method, book_id, user_id, current_page, page_size):
    a = action_operation()
    result = a.get_user_rating_rocord(method=method, user_id=user_id, book_id=book_id, current_page=current_page,
                                      page_size=page_size)
    return result

# 获取article
def api_get_article_record(method, book_id, user_id, current_page, page_size):
    a = action_operation()
    result = a.get_user_article_rocord(method=method, user_id=user_id, book_id=book_id, current_page=current_page,
                                      page_size=page_size)
    return result