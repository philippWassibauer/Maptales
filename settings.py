# -*- coding: utf-8 -*-
# Django settings for complete pinax project.

import os.path
import pinax

DATE_FORMAT = "d. m. Y"
DATETIME_FORMAT = "P - d. m. Y"

PINAX_ROOT = os.path.realpath(os.path.dirname(pinax.__file__))
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

# tells Pinax to use the default theme
PINAX_THEME = 'default'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through django.views.static.serve.
SERVE_MEDIA = DEBUG

ADMINS = (
    ('Philipp Wassibauer', 'phil@maptales.com'),
)

MANAGERS = (
    ('Philipp Wassibauer', 'phil@maptales.com'),
)

import logging
logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(filename)s %(lineno)d %(message)s',
    filename = PROJECT_ROOT+'/maptales.log',
    filemode = 'w'
)

GEOIP_PATH = '/home/philipp/Desktop/django projects/GeoIP-1.4.4/data'

SEND_BROKEN_LINK_EMAILS = False

DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'dev.db'       # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TEST_RUNNER = 'django_nose.run_gis_tests'
POSTGIS_TEMPLATE = "template_postgis"


HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = "http://localhost:8977/solr"


MAIN_BLOG_USER = "admin"
MAIN_EDITOR = "admin"

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Vienna'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

ugettext = lambda s: s
LANGUAGES = (
  ('de', u'Deutsch'),
  ('en', u'English'),
)

CMS_SEO_FIELDS = True
CMS_REDIRECTS = True

CMS_TEMPLATES = (
        ('cms_content_page.html', ugettext ('cms_info_base')),
        ('cms_right_column.html', ugettext('Right Column')),
        ('cms_left_column.html', ugettext('Left Column')),
        ('3col.html', ugettext('3 Column')),
        ('cms_full_control.html', ugettext('Use whole canvas')),
)


CMS_PLACEHOLDER_CONF = {                        
    'right-column': {
        "plugins": ('FilePlugin', 'FlashPlugin', 'LinkPlugin', 'PicturePlugin',
                    'TextPlugin', 'SnippetPlugin', 'CMSPhotologuePhotoPlugin',
                    'CMSPhotologueGalleryPlugin', 'TwitterRecentEntriesPlugin'),
        "extra_context": {"theme":"16_16"},
        "name":ugettext("right column")
    },
    
    'body': {
        "plugins": ("PicturePlugin", "GoogleMapPlugin", 'LinkPlugin', "VideoPlugin",
                    "TextPlugin", 'CMSPhotologuePhotoPlugin',
                    'CMSPhotologueGalleryPlugin', 'TwitterRecentEntriesPlugin', 'SnippetPlugin'),
        "extra_context": {"theme":"16_5"},
        "name":ugettext("body"),
    },
}


MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media')


# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/site_media/'

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'site_media/static')

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = '/site_media/static/'
CMS_MEDIA_URL = '/site_media/static/cms/'

# Additional directories which hold static files
STATICFILES_DIRS = (
    ('', os.path.join(PROJECT_ROOT, 'media')),
    ('pinax', os.path.join(PINAX_ROOT, 'media', PINAX_THEME)),
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bk-e2zv3humar79nm=j*bwc=-ymeit(8a20whp3goq4dh71t)s'


GOOGLE_MAPS_API_KEY="ABQIAAAAh-e-zeVUa3uwWsHRQfRYHRQzZ2M6v18Z7hzL43xAK5ul4PujdBSZ5V6wYLcRzoB06t2FArgeuNMbHg"


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'openid_consumer.middleware.OpenIDMiddleware',
    #'django_openidconsumer.middleware.OpenIDMiddleware',
    'account.middleware.LocaleMiddleware',
    
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    #'cms.middleware.multilingual.MultilingualURLMiddleware',
    
    'django.contrib.messages.middleware.MessageMiddleware',
    
    'django.middleware.doc.XViewMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'misc.middleware.SortOrderMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'facebook.djangofb.FacebookMiddleware',
    
    'cms.middleware.toolbar.ToolbarMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'account.middleware.AuthenticatedMiddleware',
)

AUTHENTICATED_EXEMPT_URLS = [
    r"^/v2/",
    r"^/styles/",
    r"^/mobile_login/$",
    r"^/mobile_signup/$",
    r"^/learn-more/$",
    r"^/private-beta/$",
    r"^/about/$",
    r"^/iphone-app/$",
    r"^/impressum/$",
    r"^/story/mobile-post/$",
    r"^/story/mobile-add-track-to-story/(?P<id>[0-9]+)/$",
    r"^/story/mobile-add-post-to-storyline/(?P<id>[0-9]+)/$",
    r"^/success/$",
    r"^/passphrase_check$",
    r"^/passphrase_check/$",
    r"^/photos/flash_upload/$",
    r"^/account/login/$",
    r"^/account/signup/$",
    r"^/account/password_reset",
    r"^/account/confirm_email/([\w\.-]+)/",
    r"^/account/confirm_email",
    r"^/settings/account/signup/",
    r"^/settings/account/password_reset/",
    r"^/settings/account/confirm_email/",
    r"^/socialregister/facebook/login/",
]

ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = False

if not DEBUG:
    MIDDLEWARE_CLASSES += ("django.contrib.csrf.middleware.CsrfViewMiddleware",	
                           "django.contrib.csrf.middleware.CsrfResponseMiddleware",)

ROOT_URLCONF = 'maptales.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
    os.path.join(PINAX_ROOT, "templates", PINAX_THEME),
)

DJANGO_BUILTIN_TAGS = (
    'native_tags.templatetags.native',
)

NATIVE_TAGS = (
    # Extra native contrib tags to test
    'native_tags.contrib.comparison',
    'native_tags.contrib.context',
    'native_tags.contrib.generic_content',
    'native_tags.contrib.generic_markup',
    'native_tags.contrib.hash',
    'native_tags.contrib.serializers',
    'native_tags.contrib.baseencode',
    'native_tags.contrib.regex',
    'native_tags.contrib.mapreduce',
    'native_tags.contrib.cal',
    'native_tags.contrib.math_',
    'native_tags.contrib.rand',
    #'native_tags.contrib.smart_if',
        
    # Native tags with dependencies
    'native_tags.contrib.gchart', # GChartWrapper
    'native_tags.contrib.pygmentize', # Pygments
    'native_tags.contrib.feeds', # Feedparser
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",

    "pinax.core.context_processors.pinax_settings",
        
    "notification.context_processors.notification",
    "announcements.context_processors.site_wide_announcements",
    #"account.context_processors.openid",
    "account.context_processors.account",
    "misc.context_processors.contact_email",
    "misc.context_processors.site_name",
    "misc.context_processors.domain_name",
    "messages.context_processors.inbox",
    "friends_app.context_processors.invitations",
    "misc.context_processors.combined_inbox_count",
    "misc.context_processors.settings",
    
    "django.contrib.messages.context_processors.messages",
    
    "cms.context_processors.media",
)

COMBINED_INBOX_COUNT_SOURCES = (
    "messages.context_processors.inbox",
    "friends_app.context_processors.invitations",
    "notification.context_processors.notification",
)

MAP_SCALES = (1,10,17)

INSTALLED_APPS = (
    # included
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.sites',
   'django.contrib.humanize',
   'django.contrib.markup',
   'django.contrib.gis',
   'django.contrib.sitemaps',
   'django.contrib.admin',
   'django.contrib.messages',
   
   'reversion',
   'grappelli',
   
   # external
   'notification', # must be first
   'emailconfirmation',
   'django_extensions',
   'robots',
   'friends',
   'mailer',
   'messages',
   'announcements',
   'oembed',
   'pagination',
   'threadedcomments',
   'timezones',
   #'feedutil',
   'voting',
   'tagging',
   'ajax_validation',
   'photologue',
   'flag',
   'uni_form',
   
   'analytics',
   'misc',
   'photos',
   'tag_app',

    'positions',
    'story',
   
    'account',
    'blog',
    'featured',
    'video',
    'audio',
    'profiles',
    'avatar', 
    'contact_form',
    'widgets',
    
    'geo',
    'maptales_app',
    'staticfiles',
    #'south',
    'categories',
    'treebeard',
    #'facebook_maptales',
    'activity_stream',
    
    'cms',
    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.link',
    'cms.plugins.file',
    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'cms.plugins.snippet',
    'cms.plugins.twitter',
    'mptt',
    'publisher',
    'menus',
    #'compressor',
    #'filebrowser',
    #'tinymce',
    
    'cmsplugin_photologue',
    
    'django_nose',
    
    'natural_earth',
    
    #'geonames',
    
    'chronograph',
    
    "ebgeo",
    
    'debug_toolbar',
    
    'native_tags',
    
    'test_utils',
    
    #'socialauth',
    #'openid_consumer',
    
    'socialregistration',
    
    'hitcount',
    
    'syncr.flickr',
    'syncr.youtube',
    'syncr.twitter',
    'syncr.delicious',
    'syncr.magnolia',
    
    'authsub',
    'bbauth',
    
    'brabeion',
    'voting',
    
    'audio',
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    #'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/%s/" % o.username,
}

HITCOUNT_KEEP_HIT_ACTIVE = { 'days': 7 }
HITCOUNT_HITS_PER_IP_LIMIT = 0

AUTH_PROFILE_MODULE = 'profiles.Profile'
NOTIFICATION_LANGUAGE_MODULE = 'account.Account'

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG
EMAIL_SUBJECT_PREFIX = "[Maptales] "
CONTACT_EMAIL = "office{at}maptales{dot}com"
SITE_NAME = "Maptales.com"
LOGIN_URL = "/account/login"
LOGIN_REDIRECT_URLNAME = "what_next"

LOGGING_OUTPUT_ENABLED = True
LOGGING_SHOW_METRICS = True
LOGGING_LOG_SQL = True


AVATAR_DEFAULT_URL = STATIC_URL+"images/buddy-48.gif"
AVATAR_GRAVATAR_BACKUP = False

INTERNAL_IPS = (
    '127.0.0.1',
)

ugettext = lambda s: s
LANGUAGES = (
  ('en', u'English'),
)

# URCHIN_ID = "ua-..."

CACHE_BACKEND = "locmem:///?max_entries=3000"
FEEDUTIL_SUMMARY_LEN = 60*7 # 7 hours

class NullStream(object):
    def write(*args, **kw):
        pass
    writeline = write
    writelines = write

RESTRUCTUREDTEXT_FILTER_SETTINGS = { 'cloak_email_addresses': True,
                                     'file_insertion_enabled': False,
                                     'raw_enabled': False,
                                     'warning_stream': NullStream(),
                                     'strip_comments': True,}

# if Django is running behind a proxy, we need to do things like use
# HTTP_X_FORWARDED_FOR instead of REMOTE_ADDR. This setting is used
# to inform apps of this fact
BEHIND_PROXY = False

FORCE_LOWERCASE_TAGS = True


# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass

PHOTOLOGUE_PATH = "utils.get_image_path"

FILEBROWSER_DIRECTORY = MEDIA_ROOT
FILEBROWSER_URL_FILEBROWSER_MEDIA = STATIC_URL+'/filebrowser/'
FILEBROWSER_PATH_MEDIA = os.path.join(MEDIA_ROOT, 'site_media', "filebrowser")

TINYMCE_JS_URL =  STATIC_URL+"/js/tinymce/jscripts/tiny_mce/tiny_mce_src.js"
TINYMCE_JS_ROOT = STATIC_URL+"/js/tinymce/jscripts/tiny_mce/"

URCHIN_ID = "UA-1718211-1"

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'object_resizing' : True,
    'theme_advanced_resizing': True,
    'custom_undo_redo_levels': 10,
}

