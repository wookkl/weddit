from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _

from posts.models import Post
from .models import Community
from .forms import CommunityForm


class CommunityListView(ListView):
    """Community list view definition"""

    model = Community
    queryset = Community.objects.all()
    paginate_by = 15
    paginate_orphans = 3
    template_name = "communities/list.html"
    ordering = ["-id"]
    http_method_names = ["get"]
    context_object_name = "communities"


@method_decorator(login_required, "get")
@method_decorator(login_required, "post")
class CommunityCreateView(CreateView, SuccessMessageMixin):
    """Community create view definition"""

    model = Community
    form_class = CommunityForm
    template_name = "communities/create.html"
    success_message = _("Community created successfully")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_invalid(self, form):
        errors = []
        for key in form.errors.as_data().keys():
            for error in form.errors.as_data()[key]:
                errors.append(error.message)
        return self.render_to_response(self.get_context_data(form=form, errors=errors))


class CommunityDetailView(DetailView, MultipleObjectMixin):
    """Community detail view definition"""

    model = Community
    template_name = "communities/detail.html"
    paginate_by = 3
    paginate_orphans = 1
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        object_list = Post.objects.filter(community=self.get_object())
        context = super(CommunityDetailView, self).get_context_data(
            object_list=object_list, **kwargs
        )
        return context
