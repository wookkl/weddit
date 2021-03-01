from django import forms
from django.utils.translation import gettext as _

from ckeditor_uploader.fields import RichTextUploadingFormField

from .models import Comment


class CommentForm(forms.ModelForm):
    """Comment form definition"""

    class Meta:
        model = Comment
        fields = ["comment"]
