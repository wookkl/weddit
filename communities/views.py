from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.list import MultipleObjectMixin

from core.views import form_errors_iter
from posts.models import Post

from .forms import CommunityForm
from .models import Community


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


class CommunityCreateView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
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
        errors = list(form_errors_iter(form))
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
