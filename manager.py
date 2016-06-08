from insta_manager import InstaManager
from pic_manager import PicManager
from api_manager import ApiManager
from follow_manager import FollowManager
import time
import random


class Manager:
    def __init__(self, login='brak', password='brak', category='brak', timestamp=3600):
        self.login = login
        self.password = password
        self.users_to_like = []
        self.category = category
        self.timestamp = timestamp

    def start(self):
        self.insta_manager = InstaManager(self.login, self.password)
        self.api_manager = ApiManager()
        self.follow_manager = FollowManager(self.login, self.password)
        self.pic_manager = PicManager(self.login, self.password)
        self.api_manager.start()

        self.user_id = self.api_manager.get_user_id()

    def set_category(self, category):
        self.category = category
        self.pic_manager.category = category

    def set_timestamp(self, timestamp):
        tmp = self.timestamp * int(timestamp)
        self.timestamp = tmp


    # followuje uzytkownikow, ktorzy followali nas w czasie dzialania funkcji
    # sleep_time - czas uspienia w sekundach.
    def follow4follow(self, delay):
        print("Follow4follow started...")
        initial_count = int(self.api_manager.get_self_followed_by_count())

        time.sleep(delay)

        later_count = int(self.api_manager.get_self_followed_by_count())
        if initial_count < later_count:
            difference = later_count - initial_count
            followers = self.follow_manager.get_followers(self.user_id)

            while difference > 0:
                self.insta_manager.follow(followers[difference - 1])
                difference -= 1

    # followuje wszystkich uzytkownikow z listy followersow
    def alternative_follow4follow(self):
        print("Follow4follow started...")
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
        return self.choose_users(users)

    #wybiera 10 uzytkownikow do zalajkowania
    def choose_users(self, users):
        if users.__len__() < 10:
            return users
        else:
            return random.sample(users, 10)

    def like4like(self, users):
        print ("Like4like started...")
        for user in users:
            user_name = self.follow_manager.get_user_name(user)
            media_to_like = self.api_manager.get_user_media(user_name)
            for media in media_to_like:
                self.insta_manager.like(media)

    def get_fame(self):
        while (True):
            print time.strftime("%c")
            self.pic_manager.upload()
            fame_tag_list = self.pic_manager.get_default_category_tags([])

            print("Liking and following by fame tag list started...")
            for tag in fame_tag_list[:3]:
                self.insta_manager.get_media_id_by_tag(tag)
                for media in self.insta_manager.media_by_tag:
                    self.insta_manager.like(media["id"])
                    self.insta_manager.follow(media["owner"]["id"])

            self.alternative_follow4follow()
            self.like4like(self.get_users_to_like())
            timestamp = self.timestamp + random.randint(0,300)
            print time.strftime("%c")
            print ("Next getting fame after: "+str(timestamp)+ "sec")
            time.sleep(timestamp)
