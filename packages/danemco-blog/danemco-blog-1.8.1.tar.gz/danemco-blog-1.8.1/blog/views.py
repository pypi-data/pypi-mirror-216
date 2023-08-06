from django.contrib import messages
from django.contrib.sites.models import Site
from django.db.models import Q, Case, Count, IntegerField, When
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.dates import DateDetailView, DayArchiveView, \
    MonthArchiveView, YearArchiveView, ArchiveIndexView

from . import settings as blog_settings
from .forms import CommentForm, SearchForm
from .models import Category, Article, Comment


class BaseArticleMixin(object):
    date_field = "pub_date"
    month_format = '%m'

    def get_queryset(self):
        return Article.objects.prefetch_related(
            'categories',
        ).select_related(
            'author',
        ).annotate(
            approved_comments=Count(Case(
                When(comment__approved=True, then=1),
                output_field=IntegerField(),
            )),
        ).filter(
            pub_date__lte=timezone.now(),
            sites=Site.objects.get_current()
        ).order_by(
            '-pub_date',
        )


class ArticleDetailBySlugView(BaseArticleMixin, DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        if self.object.enable_comments:
            if blog_settings.BLOG_COMMENTING_REQUIRES_LOGIN:
                login_requirement_met = self.request.user.is_authenticated()
            else:
                login_requirement_met = True

            kwargs['login_requirement_met'] = login_requirement_met

            if login_requirement_met:
                kwargs['form'] = CommentForm()

        return DetailView.get_context_data(self, **kwargs)


class ArticleDetailView(BaseArticleMixin, DateDetailView):

    def get_context_data(self, **kwargs):
        if self.object.enable_comments:
            if blog_settings.BLOG_COMMENTING_REQUIRES_LOGIN:
                login_requirement_met = self.request.user.is_authenticated()
            else:
                login_requirement_met = True

            kwargs['login_requirement_met'] = login_requirement_met

            if login_requirement_met:
                kwargs['form'] = CommentForm()

        return DateDetailView.get_context_data(self, **kwargs)


class ArticleDayArchiveView(BaseArticleMixin, DayArchiveView):
    pass


class ArticleMonthArchiveView(BaseArticleMixin, MonthArchiveView):
    pass


class ArticleYearArchiveView(BaseArticleMixin, YearArchiveView):
    pass


class ArticleArchiveView(BaseArticleMixin, ArchiveIndexView):
    allow_empty = True
    paginate_by = 5


def entries_in_category(request, slug='general'):
    category = None
    try:
        category = Category.objects.distinct().get(
            slug=slug,
            article__pub_date__lte=timezone.now(),
        )
    except Category.DoesNotExist:
        for c in Category.objects.filter(
            article__pub_date__lte=timezone.now(),
        ):
            if slugify(c.name) == slug:
                category = c
                break

    if category:
        return render(
            request,
            'blog/category_detail.html',
            {'category': category},
        )
    raise Http404('No such category')


def post_comment(request, year, month, day, slug):
    """
    Process requests to post comments on a blog article
    """
    if (
        blog_settings.BLOG_COMMENTING_REQUIRES_LOGIN and
        not request.user.is_authenticated()
    ):
        raise Http404

    site = Site.objects.get_current()
    try:
        a = Article.objects.get(
            pub_date__lte=timezone.now(),
            pub_date__year=year,
            pub_date__month=month,
            pub_date__day=day,
            slug=slug,
            sites=site,
            enable_comments=True,
        )
    except Article.DoesNotExist:
        raise Http404

    # if this method has been called via a POST request...
    if request.method == 'POST':
        # get the submitted information
        f = CommentForm(request.POST)

        # validate it
        if f.is_valid():
            # if the form passes validation, go ahead and create the comment
            c = Comment()
            c.article = a

            if blog_settings.BLOG_COMMENTING_REQUIRES_LOGIN:
                c.name = \
                    request.user.get_full_name() or request.user.get_username()
            else:
                c.name = f.cleaned_data['name']

            c.comments = f.cleaned_data['comments']
            c.save()

            if not blog_settings.BLOG_COMMENTS_AUTO_APPROVE:
                messages.success(request, "Your comment has been submitted for approval")

            # return to the original blog article
            return HttpResponseRedirect(a.get_absolute_url())
    else:
        # otherwise, this has been called with a GET request (most likely)
        f = CommentForm({})

    return render(
        request,
        'blog/article_detail.html',
        {
            'object': a,
            'form': f,
            'login_requirement_met': True,
        },
    )


def search(request, template_name='blog/search.html'):

    query = request.GET.get('query', None)
    articles = []

    if query:
        form = SearchForm(initial={'query': query})

        articles = Article.objects.filter(sites=Site.objects.get_current()).distinct()
        for bit in query.split():
            articles = articles.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(categories__name__icontains=query),
                pub_date__lte=timezone.now(),
            )
    else:
        form = SearchForm()

    return render(request, template_name, locals())
