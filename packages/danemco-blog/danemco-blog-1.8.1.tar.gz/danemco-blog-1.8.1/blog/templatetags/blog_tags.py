# Django
from django import template
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

# Project
from ..forms import SearchForm
from ..models import Article, Category
from ..feeds import LatestEntries


register = template.Library()


@register.inclusion_tag('blog/rss_feeds.html')
def insert_blog_feeds():
    """
    Add the Blog feeds. This should be in the head tag

    Tag Template :template:`blog/rss_feeds.html`

    Example::

        {% insert_blog_feeds %}

    """
    feeds = {
        'latest': LatestEntries,
    }

    feed_info = []
    for label in feeds:
        feed_info.append({'label': label, 'title': feeds[label].title})

    return {'feeds': feed_info}


@register.inclusion_tag('blog/all_articles.html', takes_context=True)
def display_all_articles(context={}):
    """
    Shows all articles that are published

    Tag Template :template:`blog/all_article.html`

    Example::

        {% display_all_articles %}

    """
    site = Site.objects.get_current()
    today = timezone.now()
    articles = Article.objects.filter(sites=site,
                                      pub_date__lte=today)

    context.update({'all_articles': articles, 'today': today})
    return context


@register.inclusion_tag('blog/_blog_search.html')
def blog_search_form():
    """
    Add in the blog search form.

    Tag Template :template:`blog/_blog_search.html`

    Example::

        {% blog_search_form %}
    """
    return {'form': SearchForm()}


@register.inclusion_tag('blog/_blog_categories.html')
def get_blog_category_list():
    """
    Get a list of all blog categoies

    Tag Template :template:`blog/_blog_categories.html`

    Example::

        {% get_blog_category_list %}
    """

    return {
        'b_categories': Category.objects.filter(
            article__isnull=False,
            article__pub_date__lte=timezone.now(),
        ).distinct().order_by('name')
    }


@register.inclusion_tag('blog/_tag_cloud.html')
def tag_cloud(max_size=5):
    """
    Makes a tag cloud out of the blog categories.

    Tag Template :template:`blog/_tag_cloud.html`

    Example::

        {% tag_cloud %}
        {% tag_cloud 3 %}

    """
    now = timezone.now()

    # 1 based not 0 based
    max_size = int(max_size) - 1

    categories = Category.objects.filter(article__pub_date__lte=now).annotate(
        articles=models.Sum(
            models.Case(
                models.When(
                    article__pub_date__lte=now,
                    then=1
                ),
                default=0,
                output_field=models.IntegerField()
            )
        )
    ).order_by('name')

    # find a good number to group the categories into
    split = categories.aggregate(s=models.StdDev('articles'),)['s']
    if split:
        split = max(round(split), 1)
    else:
        split = 1

    tags = []
    for cat in categories:
        size = int(min(round(cat.articles / split), max_size))
        tags.append((cat, size))

    return {'tags': tags}


@register.inclusion_tag('blog/_blog_nav_tree.html', takes_context=True)
def blog_nav_tree(context, year=None, month=None, article=None):
    """

    Create a navigation tree to use in the blog. This is grouped by year, month, day.
    You can also pass in the year, month or article to limit it by

    Tag Template :template:`blog/_blog_nav_tree.html`

    Example::

        {% blog_nav_tree %}
    """

    # make this return the year and month ranges.

    now = timezone.now()
    try:
        request = template.Variable('request').resolve(context)
        user_is_authenticated = request.user.is_authenticated

    except Exception:
        user_is_authenticated = False

    articles = Article.objects.filter(pub_date__lte=now).order_by('-pub_date')
    if not user_is_authenticated:
        articles = articles.exclude(private=True)

    if not year:
        year = now.year

    if not month:
        month = now.month

    return {
        'articles': articles,
        'blog_year': year,
        'blog_month': month,
        'blog_article': article,
        'is_authenticated': user_is_authenticated
    }


@register.simple_tag
def get_articles_count_for_year(date, is_auth=False):
    now = timezone.now()
    site = Site.objects.get_current()

    articles = Article.objects.filter(
        sites=site,
        pub_date__lte=now,
        pub_date__year=date.year
    ).order_by('-pub_date')

    if not is_auth:
        articles = articles.exclude(private=True)

    return articles.count()


@register.simple_tag
def get_articles_count_for_month(date, is_auth=False):

    now = timezone.now()

    site = Site.objects.get_current()

    articles = Article.objects.filter(
        sites=site,
        pub_date__lte=now,
        pub_date__year=date.year,
        pub_date__month=date.month
    ).order_by('-pub_date')

    if not is_auth:
        articles = articles.exclude(private=True)

    return articles.count()


@register.simple_tag(takes_context=True)
def get_articles_for_month(context, date):
    site = Site.objects.get_current()
    articles = Article.objects.filter(
        sites=site,
        pub_date__lte=timezone.now(),
        pub_date__year=date.year,
        pub_date__month=date.month
    ).order_by('-pub_date')

    return articles


@register.simple_tag
def get_recent_articles(count=5):
    """
    Return the most recent articles to a context variable.
    You can pass a count of how many you want to return.
    (defaults to 5 articles)

    Example::

        {% get_recent_articles as articles %}
        {% get_recent_articles 10 as articles %}
    """
    site = Site.objects.get_current()
    today = timezone.now()
    articles = Article.objects.filter(sites=site, pub_date__lte=today)

    return articles[:count]


@register.simple_tag
def is_cur_year(year, article, return_vals):

    return_vals_list = return_vals.split(",")

    now = article.pub_date

    if int(year) == int(now.year):
        return mark_safe(return_vals_list[0])
    else:
        return mark_safe(return_vals_list[1])


@register.simple_tag
def is_cur_month(year, month, article, return_vals):

    return_vals_list = return_vals.split(",")

    now = article.pub_date

    if int(year) == int(now.year) and int(month) == int(now.month):
        return mark_safe(return_vals_list[0])
    else:
        return mark_safe(return_vals_list[1])
