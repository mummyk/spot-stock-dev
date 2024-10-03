from .base import *

print("""
==========================
=== Development server ===
==========================
""")

SITE_ID = 1

# Email configuration for authentication
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = SMTP_PROVIDER  # e.g., smtp.gmail.com for Gmail
EMAIL_PORT = SMTP_PORT  # Common port for TLS
EMAIL_USE_TLS = True  # Use TLS
EMAIL_HOST_USER = EMAIL_HOST_USER  # Your email address
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD  # Your email password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Default from email address


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


# For media in development mode
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Text tenant sub directories
TENANT_SUBFOLDER_PREFIX = "clients"


CACHES = {
    "default": {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': f'{BASE_DIR}/tmp/django_cache',

    },
}

TENANT_SUBFOLDER_PREFIX = "clients"

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
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'django_app.log'),
            'formatter': 'tenant_context',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# For media in development mode
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


ROOT_URLCONF = 'core.urls'
