from insta_manager import InstaManager
from pic_manager import PicManager
from api_manager import ApiManager
from follow_manager import FollowManager
import time


class Manager:
    def __init__(self, login, password, tag_list):
        self.insta_manager = InstaManager(login, password)
        self.api_manager = ApiManager()
        self.follow_manager = FollowManager(login, password)
        self.pic_manager = PicManager()

        self.api_manager.start()

        self.user_id = self.api_manager.get_user_id()

    # followuje uzytkownikow, ktorzy followali nas w czasie dzialania funkcji
    # sleep_time - czas uspienia w sekundach.
    def follow4follow(self, sleep_time):
        initial_count = int(self.api_manager.get_followed_by_count())

        time.sleep(sleep_time)

        later_count = int(self.api_manager.get_followed_by_count())
        if initial_count < later_count:
            difference = later_count - initial_count
            followers = self.follow_manager.get_followers(self.user_id)

            while difference > 0:
                self.insta_manager.follow(followers[difference - 1])
                difference -= 1

    # followuje wszystkich uzytkownikow z listy followersow
    def alternative_follow4follow(self):
        followers = self.follow_manager.get_followers(self.user_id)

        for user in followers:
            self.insta_manager.follow(user)
