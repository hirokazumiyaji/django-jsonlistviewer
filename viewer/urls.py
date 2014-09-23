from django.conf.urls import include, patterns, url
from django.contrib import admin

urlpatterns = patterns('',
                       url('^admin/', include(admin.site.urls)),
                       url('viewer/', include('apps.viewer.urls'))
                       )
