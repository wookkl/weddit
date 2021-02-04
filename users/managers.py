from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model
from django.core.validators import ValidationError


class CustomUserManager(BaseUserManager):
    @classmethod
    def normalize_nickname(cls, nickname):
        if nickname:
            return nickname.lower()
        else:
            raise ValidationError("Nickname does not exist")

    def create_user(self, email, nickname, password=None):
        """Customize create user function"""
        if not email:
            raise ValidationError("Email does not exist")
        user = self.model(
            email=self.normalize_email(email),
            nickname=self.normalize_nickname(nickname),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None):
        """Customize create superuser function"""
        if not email:
            raise ValidationError("Email does not exist")
        superuser = self.model(
            email=self.normalize_email(email),
            nickname=self.normalize_nickname(nickname),
        )
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.set_password(password)
        superuser.save(using=self._db)
        return superuser

    def get_or_none(self, **kwargs):
        try:
            obj = self.get(**kwargs)
            return obj
        except get_user_model().DoesNotExist:
            return None
