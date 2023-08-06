from django.apps import AppConfig
from django.conf import settings


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'blog'
    verbose_name = getattr(settings, 'BLOG_APP_VERBOSE_NAME', 'Blog')
