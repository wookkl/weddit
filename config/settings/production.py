from config.settings.base import *

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["weddit.eba-be3gdpu7.ap-northeast-2.elasticbeanstalk.com"]

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["RDS_DB_NAME"],
        "USER": os.environ["RDS_USERNAME"],
        "PASSWORD": os.environ["RDS_PASSWORD"],
        "HOST": os.environ["RDS_HOSTNAME"],
        "PORT": os.environ["RDS_PORT"],
    }
}