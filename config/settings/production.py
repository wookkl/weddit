from config.settings.base import *

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["weddit.eba-be3gdpu7.ap-northeast-2.elasticbeanstalk.com"]

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("RDS_DB_NAME"),
        "USER": os.environ.get("RDS_USERNAME"),
        "PASSWORD": os.environ.get("RDS_PASSWORD"),
        "HOST": os.environ.get("RDS_HOST_NAME"),
        "PORT": os.environ.get("RDS_PORT"),
    }
}