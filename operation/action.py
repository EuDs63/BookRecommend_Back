from models.user_rating import UserRating
from models.user_collect import UserCollect
from models.user_comment import UserComment
from db_config import db_init as db
import json
from logger import create_logger
from utils.data_process import Data_Process

logger = create_logger(__name__)


class action_operation:
    def __init__(self):
        self.action_type = ['user_collect', 'user_comment', 'user_rating']

    def add_user_collect(self, user_id, book_id, content):
        user_collect = UserCollect(user_id=user_id, book_id=book_id, collect_type=content)
        db.session.add(user_collect)

    def add_user_comment(self, user_id, book_id, content):
        user_comment = UserComment(user_id=user_id, book_id=book_id, content=content)
        db.session.add(user_comment)

    def add_user_rating(self, user_id, book_id, content):
        user_rating = UserRating(user_id=user_id, book_id=book_id, rating=content)
        db.session.add(user_rating)
