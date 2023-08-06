from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.core.mail import send_mail
from django.urls import reverse

from . import settings as blog_settings


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    the_slug = property(lambda c: c.slug or slugify(c.name))

    def active_articles(self):
        return self.article_set.filter(pub_date__lte=timezone.now(), sites=Site.objects.get_current())

    def get_absolute_url(self):
        return reverse('blog-category-entries', args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Article(models.Model):
    description = models.CharField(
        max_length=160,
        help_text=("This will go in the meta description field of your blog post. "
                   "Search engines use this to help display what your post is about. "
                   "It is highly recommended that you include a description for your post."),
        blank=True,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_articles',
        limit_choices_to={"is_staff": True},
    )
    photo = models.ImageField(upload_to='images/blog/', blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    content = models.TextField()
    pub_date = models.DateTimeField(
        'publish date',
        help_text="This article will not be availible online until the publish date"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    enable_comments = models.BooleanField(blank=True, default=True)
    sites = models.ManyToManyField(Site)

    private = models.BooleanField(
        blank=True,
        default=False,
        help_text="Check this to prevent logged-out users from viewing this post."
    )

    month = lambda a: '%02i' % a.pub_date.month  # noqa: E731
    day = lambda a: '%02i' % a.pub_date.day  # noqa: E731

    def draft(self):
        return self.pub_date is None
    draft.boolean = True

    def published(self):
        return self.pub_date is not None and self.pub_date <= timezone.now()
    published.boolean = True

    def item_pubdate(self):
        return self.pub_date

    def category_list(self):
        return ", ".join(c.name for c in self.categories.all())

    def get_absolute_url(self):
        pd = self.pub_date
        y = pd.year
        m = self.month()
        d = self.day()
        return reverse('show-article', args=[y, m, d, self.slug])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pub_date',)
        unique_together = ('slug', 'pub_date')


class CommentManager(models.Manager):
    def get_approved(self):
        return self.get_queryset().filter(approved=True)


class Comment(models.Model):
    """
    This model represents comments that may be attached to a given blog article
    """

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=250, blank=True)
    comments = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=blog_settings.BLOG_COMMENTS_AUTO_APPROVE)

    objects = CommentManager()

    def __str__(self):
        return self.name

    def save(self, send_to=None, *args, **kwargs):
        """
        Issue 2951 - send the client an email when someone comments.
        """

        new_comment = self.pk is None

        super(Comment, self).save(*args, **kwargs)

        if not new_comment:
            return

        message = """%s has recently commented on your blog post "%s":

>>>>>
%s
<<<<<
""" % (self.name, self.article.title, self.comments)

        if not blog_settings.BLOG_COMMENTS_AUTO_APPROVE:
            site = Site.objects.get_current()
            change_url = reverse('admin:blog_comment_change', args=(self.id,))

            message = message + """
Comment is awaiting your approval before it is displayed, use this link to view
the details: http://%s%s
            """ % (site.domain, change_url,)

        send_to = send_to or blog_settings.BLOG_MODERATION_EMAIL
        if not isinstance(send_to, list):
            send_to = [send_to]
        send_mail('New Blog Comment',
                  message,
                  settings.DEFAULT_FROM_EMAIL,
                  send_to)

    class Meta:
        ordering = ('-date_posted', 'name')
