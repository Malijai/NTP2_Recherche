from __future__ import unicode_literals
from django.contrib import admin

from .models import Typequestion, Questionnaire, Questionntp2, Personne, Reponsentp2


class QuestionAdmin(admin.ModelAdmin):
    # admin.site.site_header = 'My admin'

    list_display = ('questionno', 'questionen')

    list_filter = ['questionnaire', 'typequestion']

    def save_model(self, request, obj, form, change):
        obj.save()


class PersonneAdmin(admin.ModelAdmin):

    list_display = ('code', 'hospcode', 'province', 'assistant','completed')

    list_filter = ['selecthosp', 'province', 'assistant', 'completed']

    def save_model(self, request, obj, form, change):
        obj.save()


admin.site.register(Typequestion)
admin.site.register(Questionnaire)
admin.site.register(Questionntp2, QuestionAdmin)
admin.site.register(Personne, PersonneAdmin)
admin.site.register(Reponsentp2)
