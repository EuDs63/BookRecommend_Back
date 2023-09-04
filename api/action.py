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

