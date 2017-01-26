from rauth import OAuth1Service
from flask import session

from settings import CONSUMER_KEY

from settings import CONSUMER_SECRET


class OAuthGoodreads(object):
    goodreads = None

    def __init__(self):
        self.goodreads = OAuth1Service(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            name='goodreads',
            request_token_url='http://www.goodreads.com/oauth/request_token',
            authorize_url='http://www.goodreads.com/oauth/authorize',
            access_token_url='http://www.goodreads.com/oauth/access_token',
            base_url='http://www.goodreads.com/'
        )

    def generate_token(self):
        return self.goodreads.get_request_token(header_auth=True)

    def get_redirect_url(self,rt):
        return self.goodreads.get_authorize_url(rt)

    def get_session(self,rt,rts):
        return self.goodreads.get_auth_session(rt,rts)

    def get_session_with_token(self,token):
        return self.goodreads.get_session(token)