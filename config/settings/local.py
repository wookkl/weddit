from config.settings.base import *

SECRET_KEY = "*m3cgd8!(cb7=7xstq7_rj0#c+8w+5q@5#64&(%bh6(!rkxk08"

ALLOWED_HOSTS = ["*"]

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")

# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, "uploads/")

MEDIA_URL = "/media/"