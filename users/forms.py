from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class CustomUserCreationForm(forms.Form):

    email = forms.CharField(
        widget=forms.EmailInput(attrs={"placeholder": _("Enter email")})
    )

    nickname = forms.CharField(
        min_length=4,
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": _("Enter nickname")}),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Enter password")})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Confirm password")})
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        is_exist = get_user_model().objects.filter(email=email).exists()
        if is_exist:
            raise forms.ValidationError(_("Email already exists"))
        return email

    def clean_nickname(self):
        nickname = self.cleaned_data["nickname"]
        is_exist = get_user_model().objects.filter(nickname=nickname.lower())
        if is_exist:
            raise forms.ValidationError(_("Nickname already exists"))
        return nickname

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 != password2:
            raise forms.ValidationError(_("Password don't match"))
        password_validation.validate_password(password2)

        return password2

    def save(self, commit=True):
        user = get_user_model().objects.create_user(
            email=self.cleaned_data["email"],
            nickname=self.cleaned_data["nickname"].lower(),
        )
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user
