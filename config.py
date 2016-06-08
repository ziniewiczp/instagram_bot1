from instagram import client

CONFIG = {
    'client_id': '8de9c50b1a904e6bae79e35665dbc786',
    'client_secret': 'cc4db1b9d36a4c398c7858f437a23007',
    'redirect_uri': 'http://localhost:8515/oauth_callback'
}

unauthenticated_api = client.InstagramAPI(**CONFIG)
