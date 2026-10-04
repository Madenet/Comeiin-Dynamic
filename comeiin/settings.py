# comeiin/settings.py
import os
from pathlib import Path

from dotenv import load_dotenv
import dj_database_url
from decouple import config


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-=f!6@&cm_%-)ay)n_d)p@)6c&@360bc6^@f67n1wavvxgs47$#'
)

DEBUG = config('DEBUG', default=False, cast=bool)

# Canonical public origin used by templates and crawler discovery.
SITE_URL = config('SITE_URL', default='https://www.comeiin.co.za').rstrip('/')


# ============================================================
# ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = [
    'comeiinworks.co.za',
    'www.comeiinworks.co.za',
    'comeiin.co.za',
    'www.comeiin.co.za',
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
    '.railway.app',
]


# ============================================================
# CSRF TRUSTED ORIGINS
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    'https://comeiin.co.za',
    'https://www.comeiin.co.za',
    'https://comeiinworks.co.za',
    'https://www.comeiinworks.co.za',
    'https://*.railway.app',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]


# ============================================================
# CORS
# ============================================================

CORS_ALLOWED_ORIGINS = [
    'https://comeiinworks.co.za',
    'https://www.comeiinworks.co.za',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
USE_X_FORWARDED_HOST = True

# ============================================================
# SESSION SETTINGS
# ============================================================

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = not DEBUG


# ============================================================
# CSRF COOKIE
# ============================================================

CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'


# ============================================================
# SSL / PROXY
# ============================================================

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False


# ============================================================
# SECURITY HEADERS
# ============================================================

if not DEBUG:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # REST API
    'rest_framework',
    'corsheaders',

    # Auth — allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # PWA
    'pwa',

    # Utilities
    'whitenoise.runserver_nostatic',

    # Project apps
    'core',
    'products',
    'quotes',
]


# ============================================================
# DJANGO SITES
# ============================================================

SITE_ID = 1


# ============================================================
# AUTHENTICATION BACKENDS
# ============================================================

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# ============================================================
# ALLAUTH — ACCOUNT
# ============================================================

ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGIN_REDIRECT_URL = '/'
ACCOUNT_SIGNUP_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

# Redirect paths — point allauth to our custom URLs
ACCOUNT_LOGIN_URL = '/accounts/login/'
ACCOUNT_LOGOUT_URL = '/accounts/logout/'
ACCOUNT_SIGNUP_URL = '/accounts/signup/'
ACCOUNT_RESET_PASSWORD_URL = '/accounts/password/reset/'


# ============================================================
# ALLAUTH — ADAPTERS (customize the flow)
# ============================================================

ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
ACCOUNT_FORMS = {
    # Use allauth's default forms — our templates just restyle them
    'login': 'allauth.account.forms.LoginForm',
    'signup': 'allauth.account.forms.SignupForm',
    'reset_password': 'allauth.account.forms.ResetPasswordForm',
}


# ============================================================
# ALLAUTH — SOCIAL
# ============================================================

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_LOGIN_ON_GET = True

# Skip the "continue" page after Google returns — send straight to home
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_STORE_TOKENS = False


# ============================================================
# GOOGLE OAUTH
# ============================================================

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
        'FETCH_USERINFO': True,
    },
}


# ============================================================
# PWA
# ============================================================

PWA_APP_NAME = 'Comeiin Works'
PWA_APP_SHORT_NAME = 'Comeiin'
PWA_APP_DESCRIPTION = 'Laboratory equipment and consumables supply'
PWA_APP_THEME_COLOR = '#0f172a'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_START_URL = '/?source=pwa'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-ZA'
PWA_APP_ORIENTATION = 'portrait'

PWA_APP_ICONS = [
    {'src': '/static/assets/pwa/icon-72.png',   'sizes': '72x72',   'type': 'image/png'},
    {'src': '/static/assets/pwa/icon-96.png',   'sizes': '96x96',   'type': 'image/png'},
    {'src': '/static/assets/pwa/icon-128.png',  'sizes': '128x128', 'type': 'image/png'},
    {'src': '/static/assets/pwa/icon-144.png',  'sizes': '144x144', 'type': 'image/png'},
    {'src': '/static/assets/pwa/icon-152.png',  'sizes': '152x152', 'type': 'image/png'},
    {'src': '/static/assets/pwa/icon-192.png',  'sizes': '192x192', 'type': 'image/png'},
    {'src': '/static/assets/pwa/icon-384.png',  'sizes': '384x384', 'type': 'image/png'},
    {'src': '/static/assets/pwa/icon-512.png',  'sizes': '512x512', 'type': 'image/png'},
]

PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/assets/pwa/icon-512.png',
        'sizes': '512x512',
        'type': 'image/png',
    },
]

PWA_SERVICE_WORKER_PATH = os.path.join(
    BASE_DIR, 'static', 'js', 'serviceworker.js'
)


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = 'comeiin.urls'


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'core.context_processors.site_metadata',
            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = 'comeiin.wsgi.application'


# ============================================================
# DATABASE
# ============================================================
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
}


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Create dirs if they don't exist
for d in STATICFILES_DIRS:
    os.makedirs(d, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
os.makedirs(MEDIA_ROOT, exist_ok=True)


# ============================================================
# UPLOAD LIMITS
# ============================================================

MAX_UPLOAD_SIZE = 314572800
DATA_UPLOAD_MAX_MEMORY_SIZE = 314572800
FILE_UPLOAD_MAX_MEMORY_SIZE = 314572800


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Johannesburg'
USE_I18N = True
USE_TZ = True


# ============================================================
# REST FRAMEWORK
# ============================================================

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}


# ============================================================
# EMAIL
# ============================================================

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

DEFAULT_FROM_EMAIL = config(
    'DEFAULT_FROM_EMAIL',
    default='Comeiin Works <Admin@comeiin.co.za>'
)
CONTACT_RECEIVER_EMAIL = config(
    'CONTACT_RECEIVER_EMAIL',
    default='Admin@comeiin.co.za'
)
SERVER_EMAIL = DEFAULT_FROM_EMAIL


# ============================================================
# WHITENOISE — compress + cache static
# ============================================================

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================
# LOGGING
# ============================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
}
