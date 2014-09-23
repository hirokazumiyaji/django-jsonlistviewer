from django.conf.urls import patterns, url

from .views import DetailDataView, DetailView, IndexView

urlpatterns = patterns('',
                       url('^$', IndexView.as_view(), name='viewer-index'),
                       url('^detail/data/(?P<path>.*)$',
                           DetailDataView.as_view(), name='viewer-detail-data'),
                       url('^detail/(?P<path>.*)$',
                           DetailView.as_view(), name='viewer-detail')
                       )
