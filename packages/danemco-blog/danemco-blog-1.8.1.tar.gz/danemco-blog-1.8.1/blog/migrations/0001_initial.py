from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(help_text='This will go in the meta description field of your blog post. Search engines use this to help display what your post is about. It is highly recommended that you include a description for your post.', max_length=160, blank=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('photo', models.ImageField(null=True, upload_to='images/blog/', blank=True)),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField(help_text='This article will not be availible online until the publish date', verbose_name='publish date')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('enable_comments', models.BooleanField(default=True, blank=True)),
                ('private', models.BooleanField(default=False, help_text='Check this to prevent logged-out users from viewing this post.', blank=True)),
                ('author', models.ForeignKey(related_name='blog_articles', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True})),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=250, blank=True)),
                ('comments', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=True)),
                ('article', models.ForeignKey(to='blog.Article', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'ordering': ('-date_posted', 'name'),
            },
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(to='blog.Category', blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='sites',
            field=models.ManyToManyField(to='sites.Site'),
        ),
        migrations.AlterUniqueTogether(
            name='article',
            unique_together={('slug', 'pub_date')},
        ),
    ]
