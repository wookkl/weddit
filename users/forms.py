from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from core.validators import alphanumeric_validator


def get_error_fields_already_exists(*fields):
    """Return FIELDS + already exists"""

    list_field = [*fields]
    string_fields = ", ".join(list_field)
    plural = "s" if len(list_field) > 1 else ""
    return forms.ValidationError(
        _(f"{string_fields} already exist{plural}".capitalize())
    )


def get_error_fields_not_match(*fields):
    """Return FIELDS + do not"""
    list_field = [*fields]
    string_fields = ", ".join(list_field)
    plural = "es" if len(list_field) > 1 else ""
    return forms.ValidationError(
        _(f"{string_fields} do{plural} not match".capitalize())
    )


class CustomUserCreateForm(forms.Form):
    """Custom user create form definition """

    email = forms.CharField(
        widget=forms.EmailInput(attrs={"placeholder": _("ENTER EMAIL")})
    )
    nickname = forms.CharField(
        min_length=4,
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": _("ENTER NICKNAME")}),
        validators=[alphanumeric_validator],
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("ENTER PASSWORD")})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": _("CONFIRM PASSWORD")},
        )
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        is_exist = get_user_model().objects.filter(email=email).exists()
        if is_exist:
            raise get_error_fields_already_exists("email")
        return email

    def clean_nickname(self):
        nickname = self.cleaned_data["nickname"]
        is_exist = get_user_model().objects.filter(nickname=nickname.lower())
        if is_exist:
            raise get_error_fields_already_exists("nickname")
        return nickname

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise get_error_fields_not_match("password")
        password_validation.validate_password(password2)
        return password2

    def save(self, commit=True):
        user = get_user_model().objects.create_user(
            email=self.cleaned_data["email"],
            nickname=self.cleaned_data["nickname"],
        )
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user


class LoginForm(forms.Form):
    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": _("ENTER EMAIL")},
        ),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": _("ENTER PASSWORD")}),
    )

    def clean(self):
        email = self.cleaned_data.get("email").lower()
        password = self.cleaned_data.get("password")
        try:
            user = get_user_model().objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                raise get_user_model().DoesNotExist
        except get_user_model().DoesNotExist:
            self.add_error("email", get_error_fields_not_match("email", "password"))


class UpdateEmailForm(forms.Form):

    new_email = forms.CharField(
        widget=forms.EmailInput(attrs={"placeholder": _("NEW EMAIL")})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("CURRENT PASSWORD")})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        return super().__init__(*args, **kwargs)

    def clean_new_email(self):
        new_email = self.cleaned_data["new_email"].lower()
        is_exist = get_user_model().objects.filter(email=new_email).exists()
        if is_exist:
            raise get_error_fields_already_exists("email")
        return new_email

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise get_error_fields_not_match
        password_validation.validate_password(password)
        return password

    def save(self, commit=True):
        self.user.email = self.cleaned_data["new_email"]
        self.user.save()
        return self.user


class UpdateNicknameForm(forms.Form):

    new_nickname = forms.CharField(
        min_length=4,
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": _("NEW NICKNAME")}),
        validators=[alphanumeric_validator],
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        return super().__init__(*args, **kwargs)

    def clean_new_nickname(self):
        new_nickname = self.cleaned_data["new_nickname"].lower()
        is_exist = get_user_model().objects.filter(nickname=new_nickname).exists()
        if is_exist:
            raise get_error_fields_already_exists("nickname")
        return new_nickname

    def save(self, commit=True):
        self.user.nickname = self.cleaned_data["new_nickname"]
        self.user.save()
        return self.user


class UpdateAvatarForm(forms.Form):
    new_avatar = forms.ImageField(required=False)

    def save(self, commit=True):
        return self.user


class UpdatePasswordForm(forms.Form):

    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("CURRENT PASSWORD")})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("NEW PASSWORD")})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": _("CONFIRM PASSWORD")},
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        return super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data["current_password"]
        if not self.user.check_password(current_password):
            raise get_error_fields_not_match("password")
        return current_password

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise get_error_fields_not_match("new password", "confirm password")
        password_validation.validate_password(password2)
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["password1"])
        self.user.save()
        return self.user


class DeleteAccountForm(forms.Form):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("CONFIRM PASSWORD")})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        return super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise get_error_fields_not_match("password")
        return password

    def save(self, commit=True):
        return self.user
