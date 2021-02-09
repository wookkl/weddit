import tempfile

from django.contrib.auth import get_user_model

from communities.models import Community

from posts.models import Post


def get_sample_user(**params):
    defaults = {
        "email": "test@gmail.com",
        "nickname": "testname",
        "password": "password123@",
    }
    defaults.update(**params)
    return get_user_model().objects.create_user(
        email=defaults["email"],
        nickname=defaults["nickname"],
        password=defaults["password"],
    )


def get_sample_community(creater=None, **params):
    defaults = {
        "creater": creater,
        "name": "testTitle",
        "description": "this is test community",
        "avatar": tempfile.NamedTemporaryFile(suffix=".jpg").name,
        "photo": tempfile.NamedTemporaryFile(suffix=".png").name,
    }
    defaults.update(params)
    return Community.objects.create(**defaults)


def get_sample_post(writer=None, community=None, **params):
    defaults = {
        "writer": writer,
        "community": community,
        "content": "sample content",
        "photo": tempfile.NamedTemporaryFile(suffix=".png").name,
    }
    defaults.update(params)
    return Post.objects.create(**defaults)
