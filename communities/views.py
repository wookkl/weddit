from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from posts.models import Post
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
class CommunityCreateView(CreateView, SuccessMessageMixin):
    """Community create view definition"""

    model = Community
    form_class = CommunityForm
    template_name = "communities/create.html"
    success_message = _("Community created successfully")

    def get_success_url(self):
        return reverse("communities:detail", kwargs={"slug": self.object.slug})

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


class CommunityDetailView(DetailView):
    """Community detail view definition"""

    model = Community
    template_name = "communities/detail.html"
    context_object_name = "community_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        community = self.get_object()
        posts = Post.objects.filter(community=community).order_by("-created_at")
        page = self.request.GET.get("page", 1)
        paginator = Paginator(posts, 10)
        try:
            paginated_posts = paginator.page(page)
        except PageNotAnInteger:
            paginated_posts = paginator.page(1)
        except EmptyPage:
            paginated_posts = paginator.page(paginator.num_pages)
        context["post_obj"] = paginated_posts
        return context
