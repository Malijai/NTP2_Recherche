from django.conf.urls import url
from .views import SelectDossier, savegh, saveghrepet, saveinstrugh, creerdossier, listedossiers, gh_csv, ghquestions_pdf
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', SelectDossier, name='SelectDossier'),
    url(r'^savegh/(?P<qid>[-\w]+)/(?P<intid>[-\w]+)/(?P<pid>[-\w]+)/$', savegh, name='savegh'),
    url(r'^saveghrepet/(?P<qid>[-\w]+)/(?P<intid>[-\w]+)/(?P<pid>[-\w]+)/$', saveghrepet, name='saveghrepet'),
    url(r'^saveinstrugh/(?P<intid>[-\w]+)/(?P<pid>[-\w]+)/$', saveinstrugh, name='saveinstrugh'),
    url(r'^new/$', creerdossier, name='creerdossier'),
    url(r'^liste/(?P<province>[-\w]+)/$', listedossiers, name='listedossiers'),
    url(r'^txt/(?P<pid>[-\w]+)', gh_csv, name='gh_csv'),
    url(r'^pdf/(?P<pk>[-\w]+)/(?P<intid>[-\w]+)/$', ghquestions_pdf, name='dogh_questions_pdf'),
]
