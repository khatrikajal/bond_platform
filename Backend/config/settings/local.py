# G:\bond_platform\Backend\config\settings\local.py
from os import getenv, path
from dotenv import load_dotenv
from .base import * # noqa
from .base import BASE_DIR

# local_env_file = path.join(BASE_DIR, ".env",".env.local")
local_env_file = path.join(BASE_DIR.parent, "envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)


# SECRET_KEY = "django-insecure-z(alis=n7f+*r8==1e1qee2z!l80j#wd#onby7pj--)u76g6xl"

SECRET_KEY = getenv("SECRET_KEY")
SITE_NAME = getenv("SITE_NAME", "Bond Platform")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = getenv("DEBUG") 

# SITE_NAME = getenv("SITE_NAME")

DEBUG = getenv("DEBUG", "False").lower() == "true"
# ALLOWED_HOSTS = ["bondplatform.com", "localhost", "127.0.0.1"]
# ALLOWED_HOSTS = ["bondplatform.com", "localhost", "127.0.0.1", "127.0.0.1:8000","93.127.206.37:8000"]
# ALLOWED_HOSTS = ["bondplatform.com", "localhost", "127.0.0.1", "127.0.0.1:8000","93.127.206.37"]
ALLOWED_HOSTS = [ "localhost", "127.0.0.1", "93.127.206.37"]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://93.127.206.37:8000",
    "https://93.127.206.37:8000",
]


# CSRF_TRUSTED_ORIGINS = ["https://bondplatform.com"]
# CSRF_TRUSTED_ORIGINS = [
#     "http://127.0.0.1:8000",
#     "http://localhost:8000",
#     "https://bondplatform.com",
#     "http://93.127.206.37:8000"
# ]



# ALLOWED_HOSTS = ['*']


ADMIN_URL = getenv("ADMIN_URL")


# EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
# EMAIL_HOST = getenv("EMAIL_HOST")
# EMAIL_PORT = getenv("EMAIL_PORT")
# DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
# DOMAIN = getenv("DOMAIN")

# Email Configuration (from .env.local)
EMAIL_BACKEND = getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_USE_SSL = getenv("EMAIL_USE_SSL", "False").lower() == "true"
EMAIL_HOST_USER = getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL", "no-reply@yourdomain.com")
ADMIN_EMAIL = getenv("ADMIN_EMAIL", "admin@yourdomain.com")
DOMAIN = getenv("DOMAIN", "localhost:8000")


MAX_UPLOAD_SIZE = 1 * 1024 * 1024  # 5MB

# JWT Settings - CRITICAL: Set the signing key
SIMPLE_JWT.update({
    "SIGNING_KEY": SECRET_KEY,  # Use the SECRET_KEY from environment
    "AUTH_COOKIE_SECURE": True,  # Allow non-HTTPS in development
    "AUTH_COOKIE_DOMAIN": None,   # No domain restriction in development
    "AUTH_COOKIE_SAMESITE": "Strict",
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),  # 1 hour for development
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # 1 day for development
})

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Celery Configuration
CELERY_BROKER_URL = getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# Development-specific settings
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",  # Enable browsable API in development
]

# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": "unique-snowflake",
#     }
# }

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    },
    "otp": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "otp-snowflake",
    },
}
