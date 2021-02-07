from django.forms.models import ModelForm

from .models import Community


class CommunityForm(ModelForm):
    """Community model form definition"""

    # the request is now available, add it to the instance data
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean
        cleaned_data["creater"] = self.request.user
        return cleaned_data

    class Meta:
        model = Community
        fields = ["name", "description", "avatar", "photo"]