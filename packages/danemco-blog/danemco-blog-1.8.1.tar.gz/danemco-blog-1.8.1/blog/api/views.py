from django.utils import timezone
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Article, Category, Comment
from .serializers import (ArticleSerializer, CategorySerializer,
                          CommentSerializer)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        qs = self.queryset.filter(
            pub_date__isnull=False,
            pub_date__lte=timezone.now(),
        )
        if not self.request.user.is_authenticated:
            qs = qs.filter(private=False)
        category = self.request.GET.get("category", "")
        if category:
            qs = qs.filter(categories__slug=category)
        return qs

    @action(detail=False)
    def latest(self, request):
        try:
            latest = self.get_queryset().latest('pub_date')
            return Response(self.get_serializer(latest).data)
        except Article.DoesNotExist:
            return Response(status=204)


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects.filter(approved=True)
    serializer_class = CommentSerializer

    def get_queryset(self):
        qs = self.queryset
        article = self.request.GET.get("article", "")
        if article:
            qs = qs.filter(article=article)
        return qs


router = DefaultRouter()

router.register("categories", CategoryViewSet, "blog-category")
router.register("articles", ArticleViewSet, "blog-article")
router.register("comments", CommentViewSet, "blog-comment")
