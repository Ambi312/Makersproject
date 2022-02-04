from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from oursite.views import UserPostRelationView

router = SimpleRouter()

router.register(r'post_relation', UserPostRelationView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('oursite.urls')),
    path('account/', include('account.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
