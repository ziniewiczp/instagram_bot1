from instagram import client
from config import CONFIG
from bottle import request

def get_media_count():
    access_token = request.session['access_token']
    if not access_token:
        return 'Missing Access Token'
    try:
        api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
        user_count = api.user().__getattribute__('counts')
        splitted_response = str(user_count).split(", 'followed_by': ", 1)
        splitted_response2 = splitted_response[0].split("{'media': ", 1)
    except Exception as e:
        print(e)
    return splitted_response2[1]

def get_followed_by_count():
    access_token = request.session['access_token']
    if not access_token:
        return 'Missing Access Token'
    try:
        api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
        user_count = api.user().__getattribute__('counts')
        splitted_response = str(user_count).split("'followed_by': ", 1)
        splitted_response2 = splitted_response[1].split(", 'follows': ", 1)
    except Exception as e:
        print(e)
    return splitted_response2[0]

def get_follows_count():
    access_token = request.session['access_token']
    if not access_token:
        return 'Missing Access Token'
    try:
        api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
        user_count = api.user().__getattribute__('counts')
        splitted_response = str(user_count).split("'followed_by': ", 1)
        splitted_response2 = splitted_response[1].split(", 'follows': ", 1)
        splitted_response3 = splitted_response2[1].split("}",1)
    except Exception as e:
        print(e)
    return splitted_response3[0]

def get_user_media_count(user_id):
    access_token = request.session['access_token']
    if not access_token:
        return 'Missing Access Token'
    try:
        api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
        user_count = api.user(user_id).__getattribute__('counts')
        splitted_response = str(user_count).split(", 'followed_by': ", 1)
        splitted_response2 = splitted_response[0].split("{'media': ", 1)
    except Exception as e:
        print(e)
    return splitted_response2[1]

def get_user_followed_by_count(user_id):
    access_token = request.session['access_token']
    if not access_token:
        return 'Missing Access Token'
    try:
        api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
        user_count = api.user(user_id).__getattribute__('counts')
        splitted_response = str(user_count).split("'followed_by': ", 1)
        splitted_response2 = splitted_response[1].split(", 'follows': ", 1)
    except Exception as e:
        print(e)
    return splitted_response2[0]

def get_user_follows_count(user_id):
    access_token = request.session['access_token']
    if not access_token:
        return 'Missing Access Token'
    try:
        api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
        user_count = api.user(user_id).__getattribute__('counts')
        splitted_response = str(user_count).split("'followed_by': ", 1)
        splitted_response2 = splitted_response[1].split(", 'follows': ", 1)
        splitted_response3 = splitted_response2[1].split("}",1)
    except Exception as e:
        print(e)
    return splitted_response3[0]