from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Post form definition"""

    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "CONTENT", "rows": 9})
    )
    photo = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ["content", "photo"]
