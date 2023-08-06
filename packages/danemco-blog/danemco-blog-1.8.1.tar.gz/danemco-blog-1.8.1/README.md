# Danemco Blog

A blog app for Django.

This app supports Django 2.0 through 3.2. If you need to use this app with
older versions of Django, you may install an older version of this app, as
noted below.

## Installation

### Step 1 of 7: Install packages

```bash
# Django 2.0 through 3.2
pip install danemco-blog

# Django 1.8 - Django 1.11
pip install danemco-blog==1.6.2

# Older Django versions
pip install danemco-blog==0.5.1
```

If you will be using the templates that come with this app, also install these
packages using pip:

```
django-bootstrap-pagination
django-compressor
django-crispy-forms
easy-thumbnails
```

### Step 2 of 7: Update settings.py

Add the following to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    'django.contrib.sites',
    'blog.apps.BlogConfig',
    ...
)
```

If you will be using the templates that come with this app, also add the
following to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    'bootstrap_pagination',
    'compressor',
    'crispy_forms',
    'easy_thumbnails',
    ...
)
```

Add the following settings:

```python
DEFAULT_FROM_EMAIL = 'john_doe@example.com'

SITE_ID = 1
```

If you will be using the templates that come with this app, also add the
following settings:

```python
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

STATICFILES_FINDERS = (
    ...
    'compressor.finders.CompressorFinder',
    ...
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'
```

### Step 3 of 7: Update urls.py

Create a URL pattern in your urls.py:

```python
from django.urls import include, path

urlpatterns = [
    ...
    path('blog/', include('blog.urls')),
    ...
]
```

### Step 4 of 7: Install a captcha app

Either `django-simple-captcha` or `django-recaptcha` will work. Follow their
respective installation guides.

### Step 5 of 7: Add the database tables

Run the following command:

```bash
python manage.py migrate
```

### Step 6 of 7: Collect the static files

Run the following command:

```python
python manage.py collectstatic
```

### Step 7 of 7: Update your project's `base.html` template (if necessary)

If you will be using the templates that come with this app, make sure your
project has a `base.html` template and that it has these blocks:

1. title

1. meta_description

1. content

1. extra_styles

1. extra_scripts (this one needs to be at the bottom in order to work properly)

## TinyMCE Integration

If your project uses [django-tinymce](https://github.com/aljosa/django-tinymce)
(in other words, if `'tinymce'` is in your `INSTALLED_APPS`), `danemco-blog`
will automatically use the `TinyMCE` widget in the admin. Otherwise, Django's
`AdminTextareaWidget` widget will be used.

## Settings

All of these are settings.py settings.

| Setting                          | Default value                                                                        | Notes                       |
| -------------------------------- | ------------------------------------------------------------------------------------ | --------------------------- |
| `BLOG_APP_VERBOSE_NAME`          | `'Blog'`                                                                             |                             |
| `BLOG_COMMENTING_REQUIRES_LOGIN` | `False`                                                                              |                             |
| `BLOG_COMMENTS_AUTO_APPROVE`     | `True`                                                                               |                             |
| `BLOG_MODERATION_EMAIL`          | `settings.DEFAULT_CONTACT_EMAIL` if present, otherwise `settings.DEFAULT_FROM_EMAIL` |                             |
| `BLOG_TITLE`                     | `Site.objects.get_current().name`                                                    | Used in the blog's RSS feed |
