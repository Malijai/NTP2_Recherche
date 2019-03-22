from django.conf.urls import url
from .views import Faitinstitution, ressource_new, RessourceDetail, rlisting, ressource_edit


urlpatterns = [
    url(r'^code/(?P<pk>[-\w]+)/$', Faitinstitution, name='Faitinstitution'),
    url(r'^code/(?P<pk>[-\w]+)/(?P<choix>[\w]*)/$', Faitinstitution, name='Faitinstitution'),
    url(r'^code/(?P<pk>[-\w]+)/(?P<choix>[\w]*)/(?P<histoire>[\w]*)/$', Faitinstitution, name='Faitinstitution'),
    url(r'ressource/new/$', ressource_new, name='ressource_new'),
    url(r'ressource/(?P<pk>[-\w]+)/edit/$', ressource_edit, name='ressource_edit'),
    url(r'ressource/(?P<pk>[-\w]+)/$', RessourceDetail.as_view(), name='ressource_detail'),
    url(r'^$', rlisting, name='listeressources'),
]