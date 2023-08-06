from django.conf import settings


BLOG_COMMENTING_REQUIRES_LOGIN = getattr(settings, 'BLOG_COMMENTING_REQUIRES_LOGIN', False)
BLOG_COMMENTS_AUTO_APPROVE = getattr(settings, 'BLOG_COMMENTS_AUTO_APPROVE', True)

try:
    BLOG_MODERATION_EMAIL = getattr(settings, 'BLOG_MODERATION_EMAIL', settings.DEFAULT_CONTACT_EMAIL)
except AttributeError:
    BLOG_MODERATION_EMAIL = settings.DEFAULT_FROM_EMAIL
