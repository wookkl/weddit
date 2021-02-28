from django import forms
from django.utils.translation import gettext as _

from .models import Comment
from posts.models import Post


class CommentForm(forms.ModelForm):
    """Comment form definition"""

    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(
                attrs={"placeholder": _("What are your thoughts?"), "rows": 3}
            )
        }
