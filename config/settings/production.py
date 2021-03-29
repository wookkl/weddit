from config.settings.base import *

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["weddit.eba-be3gdpu7.ap-northeast-2.elasticbeanstalk.com"]

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": os.environ["RDS_USERNAME"],
        "PASSWORD": os.environ["RDS_PASSWORD"],
        "HOST": os.environ["RDS_HOSTNAME"],
        "NAME": os.environ["RDS_DB_NAME"],
        "PORT": os.environ["RDS_PORT"],
    }
}

STATIC_URL = "/static/"

STATIC_ROOT = "static"

# Media files

MEDIA_URL = "/media/"

MEDIA_ROOT = "media"
