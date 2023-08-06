from django.conf.urls import re_path

from .feeds import LatestEntries
from .views import (ArticleArchiveView, ArticleDayArchiveView,
                    ArticleDetailBySlugView, ArticleDetailView,
                    ArticleMonthArchiveView, ArticleYearArchiveView,
                    entries_in_category, post_comment, search)

urlpatterns = [
    re_path(r'^rss/latest/$', LatestEntries(), name="blog-rss"),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d+?)/(?P<day>\d+?)/(?P<slug>[-\w]+)/$',
            ArticleDetailView.as_view(), name='show-article'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d+?)/(?P<day>\d+?)/$',
            ArticleDayArchiveView.as_view(), name='show-articles-on-day'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d+?)/$',
            ArticleMonthArchiveView.as_view(), name='show-articles-in-month'),
    re_path(r'^(?P<year>\d{4})/$',
            ArticleYearArchiveView.as_view(), name='show-articles-in-year'),
    re_path(r'^$',
            ArticleArchiveView.as_view(), name='recent-blog-articles'),
    re_path(r'^search/$', search, name='blog-search'),
    re_path(r'^(?P<slug>[-\w]+)/$', ArticleDetailBySlugView.as_view(), name='show-article-by-slug'),
    re_path(r'^category/(?P<slug>[-_\w]+)/$', entries_in_category, name='blog-category-entries'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d+?)/(?P<day>\d+?)/(?P<slug>[-\w]+)/comment/$', post_comment, name='blog-post-comment'),
]
