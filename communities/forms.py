from django import forms
from django.utils.translation import gettext as _

from .models import Community


class CommunityForm(forms.ModelForm):
    """Community model form definition"""

    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "NAME"}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "DESCRIPTION", "rows": 3})
    )
    avatar = forms.ImageField(required=False)
    photo = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.reqeust = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.creater = self.reqeust.user
        if commit:
            instance.save(commit)
        return instance

    def clean_name(self):
        name = self.cleaned_data["name"].lower()
        is_exist = Community.objects.filter(name=name).exists()
        if is_exist:
            raise forms.ValidationError(_("Name already exists"))
        return name

    class Meta:
        model = Community
        fields = ["name", "description", "avatar", "photo"]