from django.conf.urls import patterns, include, url


urlpatterns = patterns('aefat.aefat_pages.views',
    url(r'^$', 'aefat', name="aefat"),
    url(r'^home/$', 'aefat_home', name="aefat_home"),
)
