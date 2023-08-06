import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy


class ViewsTest(TestCase):
    fixtures = [
        'blog_test_data.json',
    ]

    def setUp(self):
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def tearDown(self):
        os.environ['RECAPTCHA_TESTING'] = 'False'

    def login(self):
        get_user_model()._default_manager.create_user(
            username='user',
            password='user',
            email='normal@example.com',
            first_name='Normal',
            last_name='User',
        )
        self.client.login(username='user', password='user')

    def rest(self, endpoint, args=[], payload=None):
        url = reverse_lazy(endpoint, args=args)
        response = self.client.get(url, payload)
        response = response.json()
        if isinstance(response, dict):
            response = response['results']
        return response

    def test_article_list(self):
        response = self.rest('blog-article-list')
        # missing prepublished article
        self.assertEqual(len(response), 5)

    def test_article_list_filter_by_category(self):
        response = self.rest('blog-article-list', [], dict(category='bar'))
        self.assertEqual(len(response), 3)

    def test_private_article(self):
        self.login()
        response = self.rest('blog-article-list')
        self.assertEqual(len(response), 6)

    def test_comments(self):
        response = self.rest('blog-comment-list')
        self.assertEqual(len(response), 2)

    def test_article_comments(self):
        response = self.rest('blog-comment-list', [], dict(article=1))
        self.assertEqual(len(response), 1)

    def test_article_comments_but_unapproved(self):
        response = self.rest('blog-comment-list', [], dict(article=2))
        self.assertEqual(len(response), 0)

    def test_article_categories(self):
        response = self.rest('blog-category-list')
        self.assertEqual(len(response), 4)
