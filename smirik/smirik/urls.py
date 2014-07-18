from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.core.urlresolvers import reverse

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'plot.views.main', name='main'),
    
    url(r'^login/$',
        'django.contrib.auth.views.login',
        name='login',
        kwargs={'template_name': 'registration/login.html'}),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        name='logout',
        kwargs={'template_name': 'registration/logout.html'}),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
