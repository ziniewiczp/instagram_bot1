from insta_manager import InstaManager
from pic_manager import PicManager
from api_manager import ApiManager
from follow_manager import FollowManager


class Manager:
    def __init__(self, login, password, tag_list):
        self.insta_manager = InstaManager(login, password, tag_list)
        self.api_manager = ApiManager()
        self.follow_manager = FollowManager(login, password)
        self.pic_manager = PicManager()

        self.api_manager.start()
        self.pic_manager.start()
