from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'photoplaces.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'photoplaces_web.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/photos_box_contains$', 'photoplaces_web.views.photos_box_contains'),
    url(r'^rest/clusters_box_contains$', 'photoplaces_web.views.clusters_box_contains'),
    url(r'^rest/clustering_run_get$', 'photoplaces_web.views.clustering_run_get'),
    url(r'^rest/cluster_get$', 'photoplaces_web.views.cluster_get'),
    url(r'^rest/cluster_get_stats$', 'photoplaces_web.views.cluster_get_stats'),
)
