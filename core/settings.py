from shutil import which
from pathlib import Path
import os
# import dj_database_url
from dotenv import load_dotenv
# from core.jazzmin_settings import JAZZMIN_SETTINGS

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# settings.py

CALLBACK_URL = os.environ.get('CALLBACK_URL')
CANCEL_ACTION = os.environ.get('CANCEL_ACTION')

PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
REDIS_URL = os.environ.get('REDIS_URL')
COMPANY_NAME = os.environ.get('COMPANY_NAME')
POSTGRES_NAME = os.environ.get('POSTGRES_NAME')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_PORT = os.environ.get('POSTGREs_PORT')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
DATABASES_URL = os.environ.get('DATABASES_URL')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True'

BACKEND_URL = os.environ.get('BACKEND_URL')
FRONTEND_URL = os.environ.get('FRONTEND_URL')
SMTP_PROVIDER = os.environ.get('SMTP_PROVIDER')
SMTP_PORT = os.environ.get('SMTP_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')


if not DEBUG:
    print("""
==========================
=== Production server ===
==========================
""")
    # Split the ALLOWED_HOSTS environment variable into a list
    allowed_hosts_env = os.environ.get('ALLOWED_HOSTS')
    if allowed_hosts_env:
        ALLOWED_HOSTS = allowed_hosts_env.split(',')
    else:
        ALLOWED_HOSTS = ['hhimanager.com', '157.245.85.81',
                         'www.hhimanager.com', '.hhimanager.com', '127.0.0.1']
else:
    print("""
==========================
=== Development server ===
==========================
""")
    ALLOWED_HOSTS = ['hhimanager.com', '157.245.85.81',
                     'www.hhimanager.com', '.hhimanager.com', '127.0.0.1']


# Application definition

SHARED_APPS = (
    'django_tenants',  # mandatory
    'tenant',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'tailwind',
    'theme',
    'home',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "allauth.mfa",
    "allauth.headless",
    "allauth.usersessions",
    "django_countries",
    "colorfield",
    "phonenumber_field",
    'django_filters',
    "users",
    "dashboard",
    "userMangment",
    "wallet",
)

TENANT_APPS = [
    # "tenant",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'tailwind',
    'theme',
    'home',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "allauth.mfa",
    "allauth.headless",
    "allauth.usersessions",
    "django_countries",
    "colorfield",
    "phonenumber_field",
    'django_filters',
    "users",
    "dashboard",
    "userMangment",
    "wallet",
]

INSTALLED_APPS = list(SHARED_APPS) + \
    [app for app in TENANT_APPS if app not in SHARED_APPS]


TENANT_MODEL = "tenant.Client"  # app.Model

TENANT_DOMAIN_MODEL = "tenant.Domain"  # app.Model
SHOW_PUBLIC_IF_NO_TENANT_FOUND = True

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'tenant.middleware.TenantMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'allauth.usersessions.middleware.UserSessionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        # set database name
        'NAME': POSTGRES_NAME,
        # set your user details
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'POST': POSTGRES_PORT
    },
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    # Adjust this path for your app's static files
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'theme/static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Tailwind CSS Config

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]
NPM_BIN_PATH = which("npm")

# AllAuth Settings

ACCOUNT_FORMS = {
    'login': 'users.forms.CustomLoginForm',
    'signup': 'users.forms.CustomSignupForm',
    'reset_password': 'users.forms.CustomResetPasswordForm',
    'change_password': 'users.forms.CustomChangePasswordForm',
}


SITE_ID = 1

# Email configuration for authentication
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = SMTP_PROVIDER  # e.g., smtp.gmail.com for Gmail
EMAIL_PORT = SMTP_PORT  # Common port for TLS
EMAIL_USE_TLS = True  # Use TLS
EMAIL_HOST_USER = EMAIL_HOST_USER  # Your email address
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD  # Your email password
DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL  # Default from email address


AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",)

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_BY_CODE_ENABLED = True
USERSESSIONS_TRACK_ACTIVITY = True
SESSION_COOKIE_AGE = 1209600  # Two weeks in seconds (default)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
ACCOUNT_SESSION_REMEMBER = True  # Ensure that the session persists
LOGIN_REDIRECT_URL = "/dashboard/"  # Redirect to the dashboard after login
ACCOUNT_LOGOUT_REDIRECT_URL = 'home'


CACHES = {
    "default": {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': f'{BASE_DIR}/tmp/django_cache',

    },
}

# LOGGING


# Ensure the log directory exists
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'tenant_context': {
            '()': 'django_tenants.log.TenantContextFilter'
        },
    },
    'formatters': {
        'tenant_context': {
            'format': '[%(schema_name)s:%(domain_url)s] '
                      '%(levelname)-7s %(asctime)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['tenant_context'],
            'formatter': 'tenant_context',
        },
        'file': {
            'level': 'INFO',  # Log INFO level and above
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'django_app.log'),
            'formatter': 'tenant_context',
        },
        'error_file': {  # New handler for error logs
            'level': 'ERROR',  # Log ERROR level and above
            'class': 'logging.FileHandler',
            # Separate error log file
            'filename': os.path.join(LOG_DIR, 'django_error.log'),
            'formatter': 'tenant_context',
        },
    },
    'root': {
        # Include error_file handler
        'handlers': ['console', 'file', 'error_file'],
        'level': 'INFO',  # Log INFO level and above
    },
    'loggers': {
        'django': {
            # Include error_file handler
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',  # Log INFO level and above
            'propagate': False,
        },
        # Optional: Add a logger for other apps or modules if needed
        # You can customize this section based on your app's structure
        # Example:
        # '<your_app_name>': {
        #     'handlers': ['console', 'file', 'error_file'],
        #     'level': 'DEBUG',  # Log DEBUG level and above for your app
        #     'propagate': False,
        # },
    },
}


# For media in development mode
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
