from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from blog.models import Article


class LatestEntries(Feed):
    """
    This class is an RSS feed that lists the most recent blog articles
    """

    def title(self):
        try:
            title = settings.BLOG_TITLE
        except AttributeError:
            title = Site.objects.get_current().name

        return title

    def link(self):
        return reverse('recent-blog-articles')

    def items(self):
        site = Site.objects.get_current()
        return Article.objects.filter(
            sites=site,
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date')[:5]

    def item_description(self, item):
        return item.content

    def item_categories(self, item):
        if item:
            return [o.name for o in item.categories.all()]
        return []
