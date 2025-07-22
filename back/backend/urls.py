"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt import views
from django.conf import settings
from django.contrib.staticfiles.urls import static # New
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.decorators.cache import cache_page        # キャッシュ用
# from backend.views import index
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('login.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/portfolio/', include('postlist.urls')),
    path('api/v1/school/',include('school.urls')),
    path('api/v1/judge/',include('judge.urls')),
    path('api/v1/auth/', include('drf_social_oauth2.urls', namespace='drf')), # google認証
    path('', include('users.urls')), #google認証
    # re_path(r'^media/(.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # re_path(r'^(?!api/|media/).*$', TemplateView.as_view(template_name='index.html')), # api見たかったらこれコメントアウトしてください
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
