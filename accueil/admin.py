from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Affichage, Publication, Projet, AuditEntree, Contrat


class ProfilInline(admin.StackedInline):
    model = Profile
    can_delete = False


class AutreprofilInline(admin.StackedInline):
    model = Projet
    can_delete = False


class EmployeInline(admin.StackedInline):
    model = Contrat
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (ProfilInline, AutreprofilInline, EmployeInline)
    list_display = ('username', 'email','first_name', 'last_name', 'is_active', 'get_province','last_login')
    #list_select_related = ('profile', )
    list_filter = ('profile__province', 'is_active')

    def get_province(self, instance):
        return instance.profile.get_province_display()
    get_province.short_description = 'Province'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request,obj)


class Pubs(admin.ModelAdmin):
    fieldsets = [
        ('Publication', {'fields': ['titre', 'reference','auteurs','annee',]}),
        ('Affichage', {'fields': ['lien','affichage', 'ordre']}),
    ]

    list_display = ('titre', 'annee','affichage','ordre')

    list_filter = ['annee','affichage']

    def save_model(self, request, obj, form, change):
        obj.save()


@admin.register(AuditEntree)
class AuditEntreeAdmin(admin.ModelAdmin):
    list_display = ['username', 'ip', 'action', 'action_time']
    list_filter = ['action','username']


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Publication, Pubs)
admin.site.register(Affichage)


