"""mbntp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.static import serve
from django.views.generic.base import RedirectView

admin.site.site_header = settings.ADMIN_SITE_HEADER

admin.autodiscover()

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login', kwargs={'redirect_authenticated_user': True}),
    path('blog/', include('blog.urls')),
    path('depot/', include('depot.urls')),
    path('dataentry/', include('dataentry.urls')),
    path('esms/', include('esms.urls')),
    path('goingh/', include('gh.urls')),
    path('viol/', include('violation.urls')),
    path('', include('accueil.urls')),
    path('grc/', include('NTP1Reprise.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('accueil/img/favicon.ico')))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
