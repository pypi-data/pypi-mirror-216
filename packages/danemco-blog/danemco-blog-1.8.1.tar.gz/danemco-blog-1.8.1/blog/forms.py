from django import forms
try:
    from captcha.fields import ReCaptchaField as CaptchaField  # Google ReCaptcha
except ImportError:
    from captcha.fields import CaptchaField  # django-simple-captcha

from .settings import BLOG_COMMENTING_REQUIRES_LOGIN


class CommentForm(forms.Form):
    """
    The standard Danemco Blog comments form
    """
    name = forms.CharField(label='Your Name')
    comments = forms.CharField(widget=forms.Textarea)
    security_code = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        if BLOG_COMMENTING_REQUIRES_LOGIN:
            del self.fields['name']
            del self.fields['security_code']


class SearchForm(forms.Form):
    query = forms.CharField(label='Look for')
