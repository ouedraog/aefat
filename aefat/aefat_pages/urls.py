from django.conf.urls import patterns, include, url


urlpatterns = patterns('aefat.aefat_pages.views',
    url(r'^$', 'aefat', name="aefat"),
)
