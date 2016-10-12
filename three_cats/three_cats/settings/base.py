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

PROJECT_ROOT = get_env_variable('TC_PROJECT_ROOT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_ROOT + '/three_cats.sqlite3',
    }
}

ALLOWED_HOSTS = [get_env_variable('TC_SITE_NAME'),]

TIME_ZONE = 'Europe/Kiev'
LANGUAGE_CODE = 'ru-RU'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = get_env_variable('TC_MEDIA_ROOT')
MEDIA_URL = '/media/'
STATIC_ROOT = get_env_variable('TC_STATIC_ROOT')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    get_env_variable('TC_ASSETS_DIR'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = get_env_variable('TC_SECRET_KEY')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [get_env_variable('TC_TEMPLATES_DIR'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.middleware.session_middleware',
    'apps.orders.middleware.info_middleware',
]

ROOT_URLCONF = 'three_cats.urls'

WSGI_APPLICATION = 'three_cats.wsgi.application'

LOCALE_PATHS = (
    get_env_variable('TC_LOCALE_DIR'),
)

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrap_pagination',
    'django_extensions',
    'crispy_forms',

    'apps.main_page',
    'apps.elephants',
    'apps.info',
    'apps.orders',
    'apps.moderation',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGES = (
    ('ru', gettext('Russian')),
    ('en', gettext('English')),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_TRANSLATION_REGISTRY = 'three_cats.translation'
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'ru'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

DELIVERY = (
    (0, gettext('* Delivery')),
    (1, gettext('Nova Poshta')),
    (2, gettext('Delivery to Odessa')),
    (3, gettext('Another embodiment')),
)

PAYMENT = (
    (0, gettext('* Payment')),
    (1, gettext('Cash on delivery')),
    (2, gettext('At stake Privat')),
    (3, gettext('Payment by courier')),
)

ORDER_STATUS = (
    (0, gettext('* Status')),
    (1, gettext('New')),
    (2, gettext('Decorated')),
    (3, gettext('Ready to ship')),
    (4, gettext('Sent')),
    (9, gettext('Archived')),
)

# Activation days for Users app.
ACTIVATION_DAYS = 3

# Password reset days for Users app.
PASSWORD_RESET_DAYS = 2

# Contact email
CONTACT_EMAIL = 'order@thecommonsen.se'
INFO_EMAIL = 'info@thecommonsen.se'

# Email config
EMAIL_USE_TLS = True
EMAIL_HOST = get_env_variable('TC_EMAIL_HOST')
EMAIL_HOST_USER = get_env_variable('TC_EMAIL_USER')
EMAIL_HOST_PASSWORD = get_env_variable('TC_EMAIL_PASSWORD')
EMAIL_PORT = 587

SMS_PUBLIC_KEY = get_env_variable('TC_SMS_PUBLIC_KEY')
SMS_PRIVATE_KEY = get_env_variable('TC_SMS_PRIVATE_KEY')
