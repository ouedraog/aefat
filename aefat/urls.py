from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url (r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),  # admin site
    url(r'^$', 'aefat.aefat_pages.views.home', name='home'),
    #url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
     url(r'^login/$', 'aefat.auth.views.login', name='login'),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^signup/$', 'aefat.auth.views.signup', name='signup'),
    url(r'^settings/$', 'aefat.core.views.settings', name='settings'),
    url(r'^settings/picture/$', 'aefat.core.views.picture', name='picture'),
    url(r'^settings/upload_picture/$', 'aefat.core.views.upload_picture', name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', 'aefat.core.views.save_uploaded_picture', name='save_uploaded_picture'),
    url(r'^settings/password/$', 'aefat.core.views.password', name='password'),
    url(r'^network/$', 'aefat.core.views.network', name='network'),
    url(r'^feeds/', include('aefat.feeds.urls')),
    url(r'^questions/', include('aefat.questions.urls')),
    url(r'^articles/', include('aefat.articles.urls')),
    url(r'^messages/', include('aefat.messages.urls')),
     url(r'^aefat/', include('aefat.aefat_pages.urls')),
    url(r'^notifications/$', 'aefat.activities.views.notifications', name='notifications'),
    url(r'^notifications/last/$', 'aefat.activities.views.last_notifications', name='last_notifications'),
    url(r'^notifications/check/$', 'aefat.activities.views.check_notifications', name='check_notifications'),
    url(r'^search/$', 'aefat.search.views.search', name='search'),
    url(r'^(?P<username>[^/]+)/$', 'aefat.core.views.profile', name='profile'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
