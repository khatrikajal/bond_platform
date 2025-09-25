from os import getenv, path
from dotenv import load_dotenv
from .base import * # noqa
from .base import BASE_DIR

local_env_file = path.join(BASE_DIR, ".env",".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)


# SECRET_KEY = "django-insecure-z(alis=n7f+*r8==1e1qee2z!l80j#wd#onby7pj--)u76g6xl"

SECRET_KEY = getenv("SECRET_KEY")
SITE_NAME = getenv("SITE_NAME", "Bond Platform")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG") 

# SITE_NAME = getenv("SITE_NAME")


ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

ADMIN_URL = getenv("ADMIN_URL")


EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
DOMAIN = getenv("DOMAIN")

MAX_UPLOAD_SIZE = 1 * 1024 * 1024  # 5MB

# JWT Settings - CRITICAL: Set the signing key
SIMPLE_JWT.update({
    "SIGNING_KEY": SECRET_KEY,  # Use the SECRET_KEY from environment
    "AUTH_COOKIE_SECURE": False,  # Allow non-HTTPS in development
    "AUTH_COOKIE_DOMAIN": None,   # No domain restriction in development
    "AUTH_COOKIE_SAMESITE": "Lax",
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),  # 1 hour for development
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # 1 day for development
})



# Celery Configuration
CELERY_BROKER_URL = getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# Development-specific settings
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",  # Enable browsable API in development
]