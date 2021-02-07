from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView

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
    fields = None
    form_class = CommunityForm
    template_name = "communities/crete.html"

    def get_success_url(self):
        return reverse_lazy("communitoes:detail", kwargs={"pk": self.object.pk})
