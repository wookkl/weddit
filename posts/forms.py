from django import forms

from communities.models import Community

from .models import Post


class PostForm(forms.ModelForm):
    """Post form definition"""

    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "CONTENT", "rows": 9, "cols": 150})
    )
    photo = forms.ImageField(required=False)

    def __init__(self, user=None, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if user:
            self.user = user
            pk_list = list(
                self.user.subscriptions.all().values_list("community__pk", flat=True)
            )
            self.fields["community"].queryset = Community.objects.filter(pk__in=pk_list)

    class Meta:
        model = Post
        fields = ["community", "content", "photo"]


class PostCreateForm(PostForm):
    """Post create form definition"""

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.writer = self.user
        if commit:
            instance.save(commit)
        return instance


class PostUpdateForm(PostForm):
    """Post form definition"""

    pass
