"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include

from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-api/', include('rest_framework.urls')),
    # path('accounts/login/', views.LoginView.as_view(), name='login'),
    # url(r'^accounts/logout/$', views.LogoutView.as_view(template_name="blog/home.html"), name='logout', kwargs={'next_page': '/'}),
    path('', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    path('polls/', include('polls.urls')),
    path('score/', include('score.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
