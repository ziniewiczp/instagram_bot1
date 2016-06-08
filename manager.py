from insta_manager import InstaManager
from pic_manager import PicManager
from api_manager import ApiManager
from follow_manager import FollowManager
import time


class Manager:
    def __init__(self, login, password, category = 'Urban'):
        self.login = login
        self.password = password
        self.users_to_like = []
        self.category = category

    def start(self):
        self.insta_manager = InstaManager(self.login, self.password)
        self.api_manager = ApiManager()
        self.follow_manager = FollowManager(self.login, self.password)
        self.pic_manager = PicManager(self.login, self.password)
        self.api_manager.start()

        self.user_id = self.api_manager.get_user_id()

    # followuje uzytkownikow, ktorzy followali nas w czasie dzialania funkcji
    # sleep_time - czas uspienia w sekundach.
    def follow4follow(self, sleep_time):
        initial_count = int(self.api_manager.get_self_followed_by_count())

        time.sleep(sleep_time)

        later_count = int(self.api_manager.get_self_followed_by_count())
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
        self.insta_manager.user_id = self.api_manager.id

    # pobiera uzytkownikow, ktorzy like'owali nasze zdjecia
    def get_users_to_like(self):
        users = []
        media = self.api_manager.get_user_self_media()
        for i in media:
            likers = self.follow_manager.get_media_likers(i)
            for j in likers:
                users.append(j)
        return users

    def like4like(self, users):
        if users.__len__() < 300:
            for user in users:
                user_name = self.follow_manager.get_user_name(user)
                media_to_like = self.api_manager.get_user_media(user_name)
                print user_name
                for media in media_to_like:
                    self.insta_manager.like(media)
        else:
            for user in range(300):
                user_name = self.follow_manager.get_user_name(users[user])
                media_to_like = self.api_manager.get_user_media(user_name)
                for media in media_to_like:
                    self.insta_manager.like(media)

    def get_fame(self):
        tag_list = self.pic_manager.get_tags(self.category, 10)

        self.pic_manager.upload(tag_list)

        for tag in tag_list[:3]:
            self.insta_manager.get_media_id_by_tag(tag)
            for media in self.insta_manager.media_by_tag:
                self.insta_manager.like(media["id"])
                self.insta_manager.follow(media["owner"]["id"])

        self.follow4follow(120)
        self.like4like(self.get_users_to_like())

        # no i to moznaby zawrzec w jakims while'u powiedzmy ale to do dogadania
        # nie testowalem, ale powinno dzialac wszystko
