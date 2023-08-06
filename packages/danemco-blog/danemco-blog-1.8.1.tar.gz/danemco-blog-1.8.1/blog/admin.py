from django.conf import settings
from django.db.models import TextField
from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Article, Category, Comment

if 'tinymce' in settings.INSTALLED_APPS:
    from tinymce.widgets import TinyMCE as TextareaWidget
else:
    from django.contrib.admin.widgets import \
        AdminTextareaWidget as TextareaWidget


class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        TextField: {'widget': TextareaWidget},
    }
    list_display = ('title', 'author', 'category_list', 'published', 'pub_date', 'enable_comments', 'total_comments',)
    list_filter = ('pub_date', 'author',)
    search_fields = ('title', 'content')
    date_hierarchy = 'pub_date'

    ordering = ("-id",)

    prepopulated_fields = {
        'slug': ('title',),
    }

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'author', 'photo', 'content', 'pub_date', 'categories', 'sites'),
        }),
        ('Advanced', {
            'fields': ('slug', 'enable_comments'),
            'classes': ('collapse',)
        }),
    )

    filter_horizontal = ("categories", )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id

        return super(ArticleAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def get_queryset(self, request):
        return Article.objects.annotate(comment_count=Count('comment'))

    def total_comments(self, obj):
        return format_html(
            '<a href="{}?article__exact={}">{}</a>',
            reverse('admin:blog_comment_changelist'),
            obj.id,
            obj.comment_count,
        )

    total_comments.admin_order_field = 'comment_count'
    total_comments.short_description = _('total comments')


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'total_articles',
    )

    prepopulated_fields = {
        'slug': ('name',),
    }

    def get_queryset(self, request):
        return Category.objects.annotate(article_count=Count('article'))

    def total_articles(self, obj):
        return format_html(
            '<a href="{}?categories__exact={}">{}</a>',
            reverse('admin:blog_article_changelist'),
            obj.id,
            obj.article_count,
        )

    total_articles.admin_order_field = 'article_count'
    total_articles.short_description = _(
        'total articles that belong to this category'
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'article',
        'name',
        'date_posted',
        'approved',
    )

    list_display_links = (
        'name',
    )


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
