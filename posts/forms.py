from django import forms
from django.utils.translation import gettext as _

from .models import Post
from communities.models import Community


class PostForm(forms.ModelForm):
    """Post form definition"""

    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "DESCRIPTION", "rows": 9})
    )
    photo = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.writer = self.request.user
        community_pk = self.request.POST.get("community_pk", None)
        try:
            instance.community = Community.objects.get(pk=community_pk)
        except Community.DoesNotExist:
            raise forms.ValidationError(_("Community object doesn/t exist"))

        if commit:
            instance.save(commit)
        return instance

    class Meta:
        model = Post
        fields = ["content", "photo"]
