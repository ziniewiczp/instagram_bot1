import json
import urllib2
from bottle import request
from instagram import client
from config import CONFIG


class ApiManager:
    def __init__(self):
        self.api_media_likes = "https://api.instagram.com/v1/media/%s/likes?access_token=%s"
        self.api_recent_media = "https://api.instagram.com/v1/users/self/media/recent/?access_token=%s"
        self.api_user_media = "https://www.instagram.com/%s/media/"

    # wywolanie po rozpoczeciu aplikacji
    def start(self):
        self.access_token = request.session['access_token']
        self.api = client.InstagramAPI(access_token=self.access_token, client_secret=CONFIG['client_secret'])
        self.id = self.get_user_id()
        self.user_name = self.get_user_name()
        # nie moze byc tej zmiennej, trzeba media count zawsze pobierac getem zeby aktualna liczbe miec
        #self.media_count = self.get_media_count()


    # dodaje do listy mediow media z zadanego jsona
    def fill_media_list(self, jsonik, media_list):
        for i in jsonik["data"]:
            media_list.append(i["id"])
        return media_list

    # zwraca liste userow ktorzy polubili zadane nasze media
    def get_list_of_users_who_liked_media(self, media):
        users_lists = []
        for i in range(media.__len__()):
            url = self.api_media_likes % (media[i], self.access_token)
            print(url)
            response = urllib2.urlopen(url).read()
            json_response = json.loads(response)
            if json_response["data"]:
                # tutaj zmienilem na j bo bylo i tak jak w poprzednim for.
                for j in json_response["data"]:
                    if j["id"] not in users_lists:
                        users_lists.append(j["id"])
        return users_lists

    # zwraca nasz username
    def get_user_name(self):
        if not self.access_token:
            return 'Missing Access Token'
        try:
            self.user_name = self.api.user().__getattribute__('username')
            return self.user_name
        except Exception as e:
            print(e)

    # zwraca nasze id
    def get_user_id(self):
        if not self.access_token:
            return 'Missing Access Token'
        try:
            user_id = self.api.user().__getattribute__('id')
            return user_id
        except Exception as e:
            print(e)

    # zwraca nasza liczbe mediow
    def get_self_media_count(self):
        return self.get_user_media_count(self.id)

    # zwraca nasza liczbe followersow
    def get_self_followed_by_count(self):
        return self.get_user_followed_by_count(self.id)

    # zwraca liczbe ktorych followujemy
    def get_self_follows_count(self):
        return self.get_user_follows_count(self.id)

    # zwraca liczbe mediow danego usera
    def get_user_media_count(self, user_id):
        if not self.access_token:
            return 'Missing Access Token'
        try:
            user_count = self.api.user(user_id).__getattribute__('counts')
            splitted_response = str(user_count).split(", 'followed_by': ", 1)
            splitted_response2 = splitted_response[0].split("{'media': ", 1)
        except Exception as e:
            print(e)
        return splitted_response2[1]

    # zwraca liczbe ktora followuje dany user
    def get_user_followed_by_count(self, user_id):
        if not self.access_token:
            return 'Missing Access Token'
        try:
            user_count = self.api.user(user_id).__getattribute__('counts')
            splitted_response = str(user_count).split("'followed_by': ", 1)
            splitted_response2 = splitted_response[1].split(", 'follows': ", 1)
        except Exception as e:
            print(e)
        return splitted_response2[0]

    # zwraca liczbe ktora followuje dany user
    def get_user_follows_count(self, user_id):
        if not self.access_token:
            return 'Missing Access Token'
        try:
            user_count = self.api.user(user_id).__getattribute__('counts')
            splitted_response = str(user_count).split("'followed_by': ", 1)
            splitted_response2 = splitted_response[1].split(", 'follows': ", 1)
            splitted_response3 = splitted_response2[1].split("}", 1)
        except Exception as e:
            print(e)
        return splitted_response3[0]

    def get_user_self_media(self):
        return self.get_user_media(self.get_user_name())

    # zwraca liste 20 ostatnich mediow uzytkownika o podanym username.
    def get_user_media(self, username):
        user_media = []
        try:
            url = self.api_user_media % username
            response = urllib2.urlopen(url).read()
            json_response = json.loads(response)
            # tutaj dodalem obcinanie tego id ale dalej nie dziala, jak bedzie zle to mozna zmienic
            for i in json_response["items"]:
                media_id = ''
                for item in i["id"]:
                    if item == '_':
                        break
                    media_id += item
                user_media.append(media_id)
        except:
            print "Exception while getting %s's media!" % username

        return user_media
