import bottle
import beaker.middleware
from manager import Manager
from bottle import route, post, request, hook, template, static_file
from instagram import client, subscriptions
from config import CONFIG, unauthenticated_api
from follow_manager import FollowManager
from my_thread import MyThread


bottle.debug(True)

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True,
}
app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)

manager = Manager()

@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

def process_tag_update(update):
    print(update)

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

# PROSZE UWAZAC BO TO WSZYSTKO JEST TAK ZAJEBISCIE KRUCHE ZE SIE W DUPIE NIE MIESCI
# ADA PROSZE NIE PISAC POLSKICH ZNAKOW BO WYCHODZI Z DUPY

@route('/')
def home():
    try:
        # TEGO URL NIE WOLNO KASOWAC BO SIE WSZYSTKO WYJEBIE
        url = unauthenticated_api.get_authorize_url(
            scope=["public_content", "comments", "likes", "follower_list", "basic", "relationships"])
        return template('index.tpl',url=url)
    except Exception as e:
        print(e)

@route('/', method="POST")
def do_home():
    # dane usera
    manager.login = request.forms.get('username')
    manager.password = request.forms.get('password')
    manager.start()
    return template('gotospecs.tpl')

@route('/specs')
def go_specs():
    return template('specs.tpl')

@route('/specs', method="POST")
def get_specs():
    # wybrane kategoria i czas
    category = request.forms.get('category')
    manager.set_category(category)
    timestamp = request.forms.get('timestamp')
    print timestamp
    manager.set_timestamp(timestamp)
    url = unauthenticated_api.get_authorize_url(
        scope=["public_content", "comments", "likes", "follower_list", "basic", "relationships"])
    return template('start.tpl', url=url)

@route('/upload')
def on_upload():
    manager.get_fame()
    #tag_list = manager.pic_manager.upload()
    return template('upload.tpl', tag_lists=[])

@route('/oauth_callback')
def on_callback():
    code = request.GET.get("code")
    if not code:
        return 'Missing code'
    try:
        access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
        if not access_token:
            return 'Could not get access token'
        request.session['access_token'] = access_token
    except Exception as e:
        print(e)
    return template('menu')

#@route('/tag_search')
#def on_tag_search():
    #manager.like4like(['fifarafka'])
    #user_id = api_manager.get_user_id()

    #thread = MyThread("urbanshot__", "kluza1", user_id, tag_list, 0)

    # zakomentowane bo nie ma instancji bota.

    # ui_manager = UserInfo(get_user_id())
    # ui_manager.followed_by_count = int(get_followed_by_count())
    #
    # time.sleep(30)
    #
    # followed_by_count = int(get_followed_by_count())
    # print 'Followed by before: %d' % ui_manager.followed_by_count
    # print 'Followed by after: %d' % followed_by_count
    #
    # if followed_by_count > ui_manager.followed_by_count:
    #     difference = followed_by_count - ui_manager.followed_by_count
    #     ui_manager.get_followed_by()
    #     while difference > 0:
    #         bot.follow(ui_manager.followed_by[difference - 1]['id'])
    #         bot.unfollow(ui_manager.followed_by[difference - 1]['id'])
    #         difference -= 1
    #
    # return template('data',
    #             posts=api_manager.get_media_count(),
    #             following=api_manager.get_follows_count(),
    #             followed=api_manager.get_followed_by_count()
    #                 )

@route('/realtime_callback')
@post('/realtime_callback')
def on_realtime_callback():
    reactor = subscriptions.SubscriptionsReactor()
    reactor.register_callback(subscriptions.SubscriptionType.TAG, process_tag_update)

    mode = request.GET.get("hub.mode")
    challenge = request.GET.get("hub.challenge")
    verify_token = request.GET.get("hub.verify_token")
    if challenge:
        return challenge
    else:
        x_hub_signature = request.header.get('X-Hub-Signature')
        raw_response = request.body.read()
        try:
            reactor.process(CONFIG['client_secret'], raw_response, x_hub_signature)
        except subscriptions.SubscriptionVerifyError:
            print("Signature mismatch")



bottle.run(app=app, host='localhost', port=8515, reloader=True)
