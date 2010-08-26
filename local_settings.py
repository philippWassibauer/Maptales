MAIN_EDITOR='admin'

EMAIL_HOST='smtp.webfaction.com'
EMAIL_HOST_USER='schmiede'
EMAIL_HOST_PASSWORD='05schmiede.#.'
EMAIL_PORT='25'
DEFAULT_FROM_EMAIL = 'schmiede@schmiede.ca'
SERVER_EMAIL = 'schmiede@schmiede.ca'


LANGUAGES = (
 ('en', u'English'),
)

DATABASE_ENGINE = 'postgresql_psycopg2'           
DATABASE_NAME = 'maptales_v2'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = 'kleini'
DATABASE_HOST = 'localhost'             # Set to empty string for localhost.
DATABASE_PORT = ''             # Set to empty string for default.

GOOGLE_MAPS_API_KEY ="ABQIAAAAh-e-zeVUa3uwWsHRQfRYHRTdYl5eH7ScdLlTteJPc2iFRlqhqBSoujXe17V2GQz48ufggMCkQbcFqQ"
#"ABQIAAAAh-e-zeVUa3uwWsHRQfRYHRRlkSyaDoYMkwmgdYEDtjn9Infy1BT3yk6zhbKntufb1E-5m3ZOHU2riQ"


#OPENID_REDIRECT_NEXT = '/accounts/openid/done/'

#OPENID_SREG = {"required": "nickname, email", "optional":"postcode,country", "policy_url": ""}
#OPENID_AX = [{"type_uri": "email", "count": 1, "required": False,
#"alias": "email"}, {"type_uri": "fullname", "count":1 , "required":
#False, "alias": "fullname"}]

TWITTER_CONSUMER_KEY = 'iVTSwaTvtaTJVwSuJnZeww'
TWITTER_CONSUMER_SECRET_KEY = 'MBSLTY9a2McJptsJ5oUP5RRXP9d56YhBeIiRgDiWfM'
TWITTER_REQUEST_TOKEN_URL = "http://twitter.com/oauth/request_token"
TWITTER_ACCESS_TOKEN_URL = "http://twitter.com/oauth/access_token"
TWITTER_AUTHORIZATION_URL = "http://twitter.com/oauth/authorize"

FACEBOOK_API_KEY = '169086736709'
FACEBOOK_SECRET_KEY = '5a38777a6eade6dd08383558eae4e34b'


AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',
                          'socialregistration.auth.TwitterAuth',
                          'socialregistration.auth.FacebookAuth',
                          )

LOGIN_REDIRECT_URL = '/'
