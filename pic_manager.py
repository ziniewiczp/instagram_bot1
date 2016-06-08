import urllib
import pynstagram
import ssl
from PIL import Image
from database.database_manager import DatabaseManager


class PicManager:
    def __init__(self, login, password):
        self.data_manager = DatabaseManager()
        self.pic_site = {
            "Swimming"  : "https://source.unsplash.com/category/people/?swimming",
            "Running"   : "https://source.unsplash.com/category/people/?running",
            "Cars"      : "https://source.unsplash.com/category/objects/?cars",
            "Sports"    : "https://source.unsplash.com/category/people/?sports",
            "Winter"    : "https://source.unsplash.com/category/nature/?winter",
            "Summer"    : "https://source.unsplash.com/category/nature/?summer",
            "Friends"   : "https://source.unsplash.com/category/people/?friends",
            "Boys"      : "https://source.unsplash.com/category/people/?boys",
            "Baby"      : "https://source.unsplash.com/category/people/?baby",
            "People"    : "https://source.unsplash.com/category/people",
            "Sea"       : "https://source.unsplash.com/category/nature/?sea",
            "Flower"    : "https://source.unsplash.com/category/nature/?flower",
            "Urban"     : "https://source.unsplash.com/category/buildings",
            "Love"      : "https://source.unsplash.com/category/people/?love",
            "Nature"    : "https://source.unsplash.com/category/nature",
            "Food"      : "https://source.unsplash.com/category/food"
        }
        self.pic_size = "/1400x1200"
        self.pic_to_upload = "pic1.jpg"
        self.login = login
        self.password = password
        self.category = "brak"

    # zwraca liste 20 defaultowych tagow LIKE COMENT FOLLOW SHOUTOUT
    def get_default_category_tags(self, list):
        list.extend(self.data_manager.get_count_tag_by_category('Likes', 5))
        list.extend(self.data_manager.get_count_tag_by_category('Comments', 5))
        list.extend(self.data_manager.get_count_tag_by_category('Follow me', 5))
        list.extend(self.data_manager.get_count_tag_by_category('Shoutout', 5))
        return list

    # zwraca liste tagow z zadanej kategorii
    # 20 tagow defaultowych i okreslone parametrem limit tagi z zadanej kategorii
    def get_tags(self, category, limit):
        list = []
        list.extend(self.data_manager.get_count_tag_by_category(category, limit))
        self.get_default_category_tags(list)
        return list

    # dodaje zdjecie
    def upload(self):
        list = self.get_tags(self.category, 10)
        context = ssl._create_unverified_context()
        category_url = self.pic_site[self.category] + self.pic_size
        urllib.urlretrieve(category_url, self.pic_to_upload, context=context)
        self.cut_image()
        with pynstagram.client(self.login, self.password) as client:
            tags = ''
            for tag in list:
                tags = tags + '#' + tag + ' '
            client.upload('pic1.jpg', tags)
        print("Photo uploaded")
        return list

    # przycina zdjecie do kwadratu
    def cut_image(self):
        img = Image.open(self.pic_to_upload)
        half_width = img.size[0] / 2
        half_height = img.size[1] / 2
        img1 = img.crop(
            (
                half_width - 450,
                half_height - 450,
                half_width + 450,
                half_height + 450
            )
        )
        img1.save(self.pic_to_upload)