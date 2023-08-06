from django.conf import settings
from django.conf.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from blog.api.views import router

urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name='homepage.html')),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^blog/', include('blog.urls')),
    re_path(r'^api/blog/', include(router.urls)),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
