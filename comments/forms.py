from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """Comment form definition"""

    class Meta:
        model = Comment
        fields = ["comment"]
