import os

gettext = lambda s: s

ADMINS = (
    ('Dmitry', 'danileyko@i.ua'),
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('TC_SECRET_KEY')

DEBUG = os.environ.get('TC_DEBUG')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', os.environ.get('TC_HOSTNAME')]

INSTALLED_APPS = [
    'cacheops',
    'modeltranslation',
    'django_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.humanize',

    'bootstrap_pagination',
    'django_extensions',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.vk',
    'debug_toolbar',

    'apps.main_page',
    'apps.elephants',
    'apps.info',
    'apps.orders',
    'apps.comments',
    'apps.gallery',
    'apps.moderation',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.middleware.session_middleware',
    'apps.orders.middleware.info_middleware',
]

ROOT_URLCONF = 'three_cats.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.environ.get('TC_TEMPLATES_PATH')],
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
                'apps.context_processors.debug',
            ],
        },
    },
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('TC_REDIS_PORT') + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    'select2': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('TC_REDIS_PORT') + "/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "select2"

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

CACHEOPS_REDIS = os.environ.get('TC_REDIS_PORT') + "/1"

WSGI_APPLICATION = 'three_cats.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('TC_DB_PATH'),
    }
}

CACHEOPS_DEFAULTS = {
    'timeout': 60*60
}

CACHEOPS = {
    'elephants.*': {'ops': 'all'},
    'comments.*': {'ops': 'all'},
    'orders.*': {'ops': 'all'},
    'info.*': {'ops': 'all'},
}

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


LANGUAGE_CODE = 'uk'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

MEDIA_ROOT = os.environ.get('TC_MEDIA_ROOT')

STATIC_ROOT = os.environ.get('TC_STATIC_ROOT')

STATICFILES_DIRS = (
    os.environ.get('TC_ASSETS_PATH'),
)

LOCALE_PATHS = (
  os.environ.get('TC_LOCALE_PATH'),
)

LANGUAGES = (
    ('ru', gettext('Russian')),
    ('uk', gettext('Ukrainian')),
    ('en', gettext('English')),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'uk'
MODELTRANSLATION_TRANSLATION_REGISTRY = 'three_cats.translation'
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'uk'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

DELIVERY = (
    (0, gettext('Warehouse-to-warehouse delivery at the nearest Nova Poshta branch (in Ukraine);')),
    (1, gettext('Nova Poshta door-to-door delivery (in Ukraine);')),
    (3, gettext('Worldwide Delivery.')),
    (2, gettext('In showroom')),
    (4, gettext('Justin')),
)

PAYMENT = (
    (3, gettext('Pay by card (Visa, MasterCard);')),
    (1, gettext('MonoBank (Ukraine only);')),
    (2, gettext('PrivatBank (Ukraine only);')),
    (0, gettext('Cash on delivery upon receipt of order at the Nova Poshta branch;')),
    (5, gettext('Cash in showroom')),
)

# Discount for regular users.
DISCOUNT_PHONE = int(os.environ.get('TC_DISCOUNT_PHONE'))

# Contact email
CONTACT_EMAIL = 'catcult.club@gmail.com'
INFO_EMAIL = 'catcult.club@gmail.com'

# Email config
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('TC_EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('TC_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('TC_EMAIL_PASSWORD')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = os.environ.get('TC_EMAIL_ADDR')
SERVER_EMAIL = os.environ.get('TC_EMAIL_ADDR')

SMS_PUBLIC_KEY = os.environ.get('TC_SMS_PUBLIC_KEY')
SMS_PRIVATE_KEY = os.environ.get('TC_SMS_PRIVATE_KEY')

PRIVAT_CARD = os.environ.get('TC_PRIVAT_CARD')
MONO_CARD = os.environ.get('TC_MONO_CARD')
PRIVAT_NAME = os.environ.get('TC_PRIVAT_NAME')
MONO_NAME = os.environ.get('TC_MONO_NAME')

LIQPAY_PUBLIC_KEY = os.environ.get('TC_LIQPAY_PUBLIC_KEY')
LIQPAY_PRIVATE_KEY = os.environ.get('TC_LIQPAY_PRIVATE_KEY')

LIQPAY_CALLBACK = os.environ.get('TC_LIQPAY_CALLBACK')
LIQPAY_SUCCESS = os.environ.get('TC_LIQPAY_SUCCESS')

STOCKS_TYPES = (
    (0, 'Unconditional'),
    (1, 'Order items count'),
    (2, 'Conditional')
)

# 0 - image, 1 - text
MENU_LAYOUT = 0

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

INTERNAL_IPS = [
    '127.0.0.1',
]

LOGIN_REDIRECT_URL = 'main_page'

DJANGORESIZED_DEFAULT_QUALITY = 90

NOVA_POSHTA_API = os.environ.get('TC_NOVA_POSHTA_API')

