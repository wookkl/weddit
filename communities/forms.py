from django.forms import models
from django import forms

from .models import Community


class CommunityForm(models.ModelForm):
    """Community model form definition"""

    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "NAME"}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "DESCRIPTION", "rows": 3})
    )
    avatar = forms.ImageField(required=False)
    photo = forms.ImageField(required=False)

    # the request is now available, add it to the instance data
    def __init__(self, *args, **kwargs):
        self.reqeust = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.creater = self.reqeust.user
        if commit:
            instance.save(commit)
        return instance

    class Meta:
        model = Community
        fields = ["name", "description", "avatar", "photo"]