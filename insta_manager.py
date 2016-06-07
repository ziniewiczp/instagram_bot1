import requests
import datetime
import json


class InstaManager:

    url = 'https://www.instagram.com/'
    url_tag = 'https://www.instagram.com/explore/tags/'
    url_likes = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'
    url_followers = 'https://www.instagram.com/web/friendships/followers/'

    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    accept_language = 'pl;q=0.8,en-US;q=0.6,en;q=0.4'

    # Log setting.
    log_file_path = ''
    log_file = 0

    # Other.
    media_by_tag = 0
    login_status = False

    def __init__(self, login, password):
        self.s = requests.Session()

        self.user_login = login.lower()
        self.user_password = password

        self.media_by_tag = []

        now_time = datetime.datetime.now()
        print 'Starting at %s:' % (now_time.strftime("%d.%m.%Y %H:%M"))
        self.login()

    def login(self):
            print 'Trying to login by %s...' % self.user_login
            self.s.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1',
                                   'ig_vw': '1920', 'csrftoken': '',
                                   's_network': '', 'ds_user_id': ''})
            self.login_post = {'username': self.user_login,
                               'password': self.user_password}
            self.s.headers.update({'Accept-Encoding': 'gzip, deflate',
                                   'Accept-Language': self.accept_language,
                                   'Connection': 'keep-alive',
                                   'Content-Length': '0',
                                   'Host': 'www.instagram.com',
                                   'Origin': 'https://www.instagram.com',
                                   'Referer': 'https://www.instagram.com/',
                                   'User-Agent': self.user_agent,
                                   'X-Instagram-AJAX': '1',
                                   'X-Requested-With': 'XMLHttpRequest'})
            r = self.s.get(self.url)
            self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
            login = self.s.post(self.url_login, data=self.login_post,
                                allow_redirects=True)
            self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
            self.csrftoken = login.cookies['csrftoken']

            if login.status_code == 200:
                r = self.s.get('https://www.instagram.com/')
                finder = r.text.find(self.user_login)
                if finder != -1:
                    self.login_status = True
                    print 'Looks like login by %s succeedded!' % self.user_login
                else:
                    self.login_status = False
                    print 'Login error! Check your login data!'
            else:
                print 'Login error! Connection error!'

    def logout(self):
        try:
            logout_post = {'csrfmiddlewaretoken': self.csrftoken}
            logout = self.s.post(self.url_logout, data=logout_post)
            print "Logged out!"
            self.login_status = False
        except:
            print "Logout error!"

    # wyszukiwanie id mediow pasujacych do podanego taga
    def get_media_id_by_tag(self, tag):
        if self.login_status:
            print "Getting media id by tag: %s..." % tag
            if self.login_status == 1:
                url_tag = '%s%s%s' % (self.url_tag, tag, '/')
                try:
                    r = self.s.get(url_tag)
                    text = r.text

                    finder_text_start = ('<script type="text/javascript">'
                                         'window._sharedData = ')
                    finder_text_start_len = len(finder_text_start) - 1
                    finder_text_end = ';</script>'

                    all_data_start = text.find(finder_text_start)
                    all_data_end = text.find(finder_text_end, all_data_start + 1)
                    json_str = text[(all_data_start + finder_text_start_len + 1) \
                        : all_data_end]
                    all_data = json.loads(json_str)

                    self.media_by_tag = list(all_data['entry_data']['TagPage'][0] \
                                                 ['tag']['media']['nodes'])

                    print "Found %d posts." % len(self.media_by_tag)
                except:
                    self.media_by_tag = []
                    print "Exception while getting media by tag %s!" % tag
            else:
                return 0

    def like(self, media_id):
        if self.login_status:
            url_likes = self.url_likes % media_id
            try:
                like = self.s.post(url_likes)
                print "Liked media with id: %s" % media_id
            except:
                print "Exception while liking media with id: %s" % media_id
                like = 0
            return like

    def unlike(self, media_id):
        if self.login_status:
            url_unlike = self.url_unlike % media_id
            try:
                unlike = self.s.post(url_unlike)
                print "Unliked media with id: %s" % media_id
            except:
                print "Exception while unliking media with id: %s" % media_id
                unlike = 0
            return unlike

    def follow(self, user_id):
        if self.login_status:
            url_follow = self.url_follow % user_id
            try:
                follow = self.s.post(url_follow)
                if follow.status_code == 200:
                    print "Followed user with id: %s." % user_id
                return follow
            except:
                print "Exception while following user with id: %s." % user_id
        return False

    def unfollow(self, user_id):
        if self.login_status:
            url_unfollow = self.url_unfollow % user_id
            try:
                unfollow = self.s.post(url_unfollow)
                if unfollow.status_code == 200:
                    print "Unfollowed user with id: %s." % user_id
                return unfollow
            except:
                print "Exception while unfollowing user with id: %s." % user_id
        return False

    def comment(self, media_id, comment_text):
        if self.login_status:
            comment_post = {'comment_text': comment_text}
            url_comment = self.url_comment % media_id
            try:
                comment = self.s.post(url_comment, data=comment_post)
                if comment.status_code == 200:
                    print 'Written: "%s" under post with id: %s.' % (comment_text, media_id)
                return comment
            except:
                print "Except while commenting media with id %s!" % media_id
        else:
            print "Login status error"
        return False
