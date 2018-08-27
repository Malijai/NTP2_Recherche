from django.conf.urls import url
from .views import Faitinstitution


urlpatterns = [
    url(r'^code/(?P<choix>[\w]*)/(?P<histoire>[\w]*)/$',Faitinstitution, name='Faitinstitution'),
]
