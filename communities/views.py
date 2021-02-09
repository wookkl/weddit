from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView

from .models import Community
from .forms import CommunityForm


class CommunityListView(ListView):
    """Community list view definition"""

    model = Community
    queryset = Community.objects.all()
    paginate_by = 10
    paginate_orphans = 5
    template_name = "communities/list.html"
    ordering = ["-id"]
    http_method_names = ["get"]


@method_decorator(login_required, "get")
@method_decorator(login_required, "post")
class CommunityCreateView(CreateView):
    """Community create view definition"""

    model = Community
    form_class = CommunityForm
    template_name = "communities/create.html"

    def get_success_url(self):
        return reverse("communities:detail", kwargs={"slug": self.object.slug})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class CommunityDetailView(DetailView):
    """Community detail view definition"""

    model = Community
    template_name = "communities/detail.html"
    context_object_name = "community_obj"
