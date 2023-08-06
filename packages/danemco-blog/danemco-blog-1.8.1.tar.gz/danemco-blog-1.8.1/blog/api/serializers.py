from rest_framework import serializers
from ..models import Category, Article, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class ArticleSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "description",
            "title",
            "slug",
            "author",
            "photo",
            "categories",
            "content",
            "pub_date",
            "date_updated",
            "comment_count",
        )

    categories = CategorySerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()

    def get_comment_count(self, instance):
        return instance.comment_set.count()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "article", "name", "comments", "date_posted")
