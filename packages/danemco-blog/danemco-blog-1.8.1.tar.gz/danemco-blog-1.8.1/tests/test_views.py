import os
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment


class ViewsTest(TestCase):
    fixtures = [
        'blog_test_data.json',
    ]

    def get_user_types(self):
        for user_type, credentials in self.user_types.items():
            if credentials:
                self.client.login(**credentials)

            yield user_type

    def setUp(self):
        normal_credentials = {
            'username': 'normal_user',
            'password': 'testing!',
        }

        get_user_model()._default_manager.create_user(
            username=normal_credentials['username'],
            password=normal_credentials['password'],
            email='normal@example.com',
            first_name='Normal',
            last_name='User',
        )

        staff_credentials = {
            'username': 'staff_user',
            'password': 'testing!',
        }

        staff_user = get_user_model()._default_manager.create_user(
            username=staff_credentials['username'],
            password=staff_credentials['password'],
            email='staff@example.com',
            first_name='Staff',
            last_name='User',
        )

        staff_user.is_staff = True
        staff_user.save()

        self.user_types = OrderedDict([
            ('anonymous', None),
            ('normal', normal_credentials),
            ('staff', staff_credentials),
        ])

        os.environ['RECAPTCHA_TESTING'] = 'True'

    def tearDown(self):
        os.environ['RECAPTCHA_TESTING'] = 'False'

    def test_category_entries(self):
        categories = [
            {
                'url': reverse('blog-category-entries', args=['foo']),
                'expected_status_code': 200,
            },
            {
                # The only article with this category is the one with a
                # future publish date.
                'url': reverse('blog-category-entries', args=['baz']),
                'expected_status_code': 404,
            },
        ]

        for user_type in self.get_user_types():
            for category in categories:
                response = self.client.get(category['url'])
                self.assertEqual(
                    response.status_code,
                    category['expected_status_code']
                )

    def test_post_comment(self):
        tests = [
            {
                'url': reverse(
                    'blog-post-comment',
                    args=['2016', '12', '31', 'awesome-article']
                ),
                'article_slug': 'awesome-article',
                'expected_status_code': 302,
            },
            {
                'url': reverse(
                    'blog-post-comment',
                    args=['2017', '01', '01', 'cool-article']
                ),
                'article_slug': 'cool-article',
                'expected_status_code': 404,
            },
            {
                'url': reverse(
                    'blog-post-comment',
                    args=['2099', '12', '31', 'futuristic-article']
                ),
                'article_slug': 'futuristic-article',
                'expected_status_code': 404,
            },
        ]

        for user_type in self.get_user_types():
            for test in tests:
                total_comments_before = Comment.objects.filter(
                    article__slug=test['article_slug'],
                ).count()

                response = self.client.post(test['url'], {
                    'name': 'Test User',
                    'comments': 'This is a test comment.',
                    'recaptcha_response_field': 'PASSED',
                })
                self.assertEqual(
                    response.status_code,
                    test['expected_status_code']
                )

                total_comments_after = Comment.objects.filter(
                    article__slug=test['article_slug'],
                ).count()

                if test['expected_status_code'] == 302:
                    self.assertEqual(
                        total_comments_after,
                        total_comments_before + 1
                    )
                else:
                    self.assertEqual(
                        total_comments_after,
                        total_comments_before
                    )

    def test_recent_articles(self):
        url = reverse('recent-blog-articles')

        for user_type in self.get_user_types():
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

            # The article with a future publish date should not be
            # included.
            self.assertEqual(len(response.context['object_list']), 5)

    def test_rss(self):
        url = reverse('blog-rss')

        for user_type in self.get_user_types():
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_search(self):
        url = reverse('blog-search')

        for user_type in self.get_user_types():
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context['articles']), 0)

            response = self.client.get(url, {'query': 'awesome'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context['articles']), 1)
            self.assertEqual(response.context['articles'][0].pk, 1)

            response = self.client.get(url, {'query': 'futuristic'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context['articles']), 0)

    def test_show_article_and_show_article_by_slug(self):
        articles = [
            {
                'urls': [
                    reverse(
                        'show-article',
                        args=['2016', '12', '31', 'awesome-article']
                    ),
                    reverse(
                        'show-article-by-slug',
                        args=['awesome-article']
                    ),
                ],
                # This article has comments enabled.
                'expected_comments_form_status': 'present',
                'expected_comments_total': 1,
            },
            {
                'urls': [
                    reverse(
                        'show-article',
                        args=['2017', '01', '01', 'brilliant-article']
                    ),
                    reverse(
                        'show-article-by-slug',
                        args=['brilliant-article']
                    ),
                ],
                # This article has comments enabled.
                'expected_comments_form_status': 'present',
                # This article has 1 comment, but it is not approved.
                'expected_comments_total': 0,
            },
            {
                'urls': [
                    reverse(
                        'show-article',
                        args=['2017', '01', '01', 'cool-article']
                    ),
                    reverse(
                        'show-article-by-slug',
                        args=['cool-article']
                    ),
                ],
                # This article has comments disabled.
                'expected_comments_form_status': 'absent',
                # 1 comment was made and approved before this article
                # had comments disabled.
                'expected_comments_total': 1,
            },
            {
                'urls': [
                    reverse(
                        'show-article',
                        args=['2017', '03', '01', 'excellent-article']
                    ),
                    reverse(
                        'show-article-by-slug',
                        args=['excellent-article']
                    ),
                ],
                # This article has comments disabled.
                'expected_comments_form_status': 'absent',
                'expected_comments_total': None,
            },
        ]

        for user_type in self.get_user_types():
            for article in articles:
                for url in article['urls']:
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, 200)

                    if article['expected_comments_total'] is None:
                        self.assertNotIn('comments', response.context)
                    else:
                        self.assertEqual(
                            len(response.context['comments']),
                            article['expected_comments_total']
                        )

                    if article['expected_comments_form_status'] == 'present':
                        self.assertContains(response, 'Post Comment')
                    else:
                        self.assertNotContains(response, 'Post Comment')

    def test_show_articles_on_day(self):
        dates = [
            {
                'url': reverse(
                    'show-articles-on-day',
                    args=['2016', '12', '31']
                ),
                'expected_status_code': 200,
                'expected_articles_total': 1,
            },
            {
                'url': reverse(
                    'show-articles-on-day',
                    args=['2017', '01', '01']
                ),
                'expected_status_code': 200,
                'expected_articles_total': 2,
            },
            {
                'url': reverse(
                    'show-articles-on-day',
                    args=['2017', '01', '02']
                ),
                'expected_status_code': 404,
            },
        ]

        for user_type in self.get_user_types():
            for date in dates:
                response = self.client.get(date['url'])
                self.assertEqual(
                    response.status_code,
                    date['expected_status_code']
                )

                if date['expected_status_code'] == 200:
                    self.assertEqual(
                        len(response.context['object_list']),
                        date['expected_articles_total']
                    )

    def test_show_articles_in_month(self):
        dates = [
            {
                'url': reverse(
                    'show-articles-in-month',
                    args=['2016', '12']
                ),
                'expected_status_code': 200,
                'expected_articles_total': 1,
            },
            {
                'url': reverse(
                    'show-articles-in-month',
                    args=['2017', '01']
                ),
                'expected_status_code': 200,
                'expected_articles_total': 3,
            },
            {
                'url': reverse(
                    'show-articles-in-month',
                    args=['2017', '02']
                ),
                'expected_status_code': 404,
            },
        ]

        for user_type in self.get_user_types():
            for date in dates:
                response = self.client.get(date['url'])
                self.assertEqual(
                    response.status_code,
                    date['expected_status_code']
                )

                if date['expected_status_code'] == 200:
                    self.assertEqual(
                        len(response.context['object_list']),
                        date['expected_articles_total']
                    )

    def test_show_articles_in_year(self):
        dates = [
            {
                'url': reverse(
                    'show-articles-in-year',
                    args=['2015']
                ),
                'expected_status_code': 404,
            },
            {
                'url': reverse(
                    'show-articles-in-year',
                    args=['2016']
                ),
                'expected_status_code': 200,
                'expected_months_total': 1,
            },
            {
                'url': reverse(
                    'show-articles-in-year',
                    args=['2017']
                ),
                'expected_status_code': 200,
                'expected_months_total': 2,
            },
        ]

        for user_type in self.get_user_types():
            for date in dates:
                response = self.client.get(date['url'])
                self.assertEqual(
                    response.status_code,
                    date['expected_status_code']
                )

                if date['expected_status_code'] == 200:
                    self.assertEqual(
                        len(response.context['date_list']),
                        date['expected_months_total']
                    )
