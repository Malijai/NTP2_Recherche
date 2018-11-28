from django.conf.urls import url
from .views import select_personne, saverepetntp2, saventp2, questions_pdf, ffait_csv, decrypt, verifie_csv, \
    creerdossierntp2, fdetemps
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', select_personne, name='SelectPersonne'),
    url(r'^saverepetntp2/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/$', saverepetntp2, name='saverepetntp2'),
    url(r'^saventp2/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/$', saventp2, name='saventp2'),
    url(r'^decrypt/(?P<pid>[-\w]+)', decrypt, name='decrypt'),
    url(r'^login/', auth_views.login, name='login',
        kwargs={'redirect_authenticated_user': True}),
    url(r'^pdf/(?P<pk>[-\w]+)/$', questions_pdf, name='do_questions_pdf'),
    url(r'^txt/(?P<pid>[-\w]+)', verifie_csv, name='verifie_csv'),
    url(r'^csv/$', ffait_csv, name='do_csv'),
    url(r'^new/$', creerdossierntp2, name='creerdossierntp2'),
    url(r'^fdt/$', fdetemps, name='do_fdt'),
]
