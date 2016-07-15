import os

from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    """
    Get the environment variable or return exception

    """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

gettext = lambda s: s

ADMINS = (
    ('Dmytry', 'danileyko@i.ua'),
)

MANAGERS = ADMINS

PROJECT_ROOT = get_env_variable('CS_PROJECT_ROOT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_ROOT + '/three_cats.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = [get_env_variable('CS_SITE_NAME')]

TIME_ZONE = 'Europe/Kiev'
LANGUAGE_CODE = 'ru-RU'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = get_env_variable('CS_MEDIA_ROOT')
MEDIA_URL = '/media/'
STATIC_ROOT = get_env_variable('CS_STATIC_ROOT')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    get_env_variable('CS_ASSETS_DIR'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = get_env_variable('CS_SECRET_KEY')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'job_board.apps.users.middleware.UserTypeMiddleware',
)

ROOT_URLCONF = 'three_cats.urls'

WSGI_APPLICATION = 'three_cats.wsgi.application'

TEMPLATE_DIRS = (
    get_env_variable('CS_TEMPLATES_DIR'),
)

LOCALE_PATHS = (
    get_env_variable('CS_LOCALE_DIR'),

)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli',
    'django.contrib.admin',

    'crispy_forms',
    'south',
    'modeltranslation',

    'apps.main_page',
    'apps.elephants',
    'apps.info',
    'apps.orders',

)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_TRANSLATION_REGISTRY = 'three_cats.translation'
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'ru'

CRISPY_TEMPLATE_PACK = 'bootstrap'

DELIVERY = (
    (0, gettext('New Post')),
    (1, gettext('Delivery to Odessa')),
    (2, gettext('Another embodiment')),
)

PAYMENT = (
    (0, gettext('Cash on delivery')),
    (1, gettext('At stake Privat')),
    (2, gettext('Payment by courier')),
)

ORDER_STATUS = (
    (0, gettext('New')),
    (1, gettext('Decorated')),
    (2, gettext('Ready to ship')),
    (3, gettext('Sent')),
)

# Disable South migrations when running tests.
SOUTH_TESTS_MIGRATE = False

# Activation days for Users app.
ACTIVATION_DAYS = 3

# Password reset days for Users app.
PASSWORD_RESET_DAYS = 2

# Contact email
CONTACT_EMAIL = 'order@thecommonsen.se'
INFO_EMAIL = 'info@thecommonsen.se'

# Email config
EMAIL_USE_TLS = True
EMAIL_HOST = get_env_variable('CS_EMAIL_HOST')
EMAIL_HOST_USER = get_env_variable('CS_EMAIL_USER')
EMAIL_HOST_PASSWORD = get_env_variable('CS_EMAIL_PASSWORD')
EMAIL_PORT = 587
