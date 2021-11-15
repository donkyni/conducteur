from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from conducteurs.models import User, Droits, Profils, DroitsProfils, Station, Conducteur


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'pseudo', 'nom', 'prenom', 'adresse',
            'telephone', 'avatar', 'sexe',
        )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'pseudo', 'nom', 'prenom', 'adresse',
            'telephone', 'avatar', 'sexe', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class DroitsAdmin(admin.ModelAdmin):
    list_display = ('nom', 'archive')
    list_filter = ('nom',)
    ordering = ('nom',)
    search_fields = ('nom',)


admin.site.register(Droits, DroitsAdmin)


class ProfilsAdmin(admin.ModelAdmin):
    list_display = ('nom', 'archive')
    list_filter = ('nom',)
    ordering = ('nom',)
    search_fields = ('nom',)


admin.site.register(Profils, ProfilsAdmin)


class DroitsProfilsAdmin(admin.ModelAdmin):
    list_display = ('profil', 'droit', 'ecriture', 'lecture', 'modification', 'suppression')
    list_filter = ('profil', 'droit')
    ordering = ('profil',)
    search_fields = ('profil',)


admin.site.register(DroitsProfils, DroitsProfilsAdmin)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'pseudo', 'nom', 'prenom', 'adresse',
        'telephone', 'profil', 'avatar', 'sexe', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'nom')
    fieldsets = (
        (None, {'fields': ('pseudo', 'password')}),
        ('Personal info', {'fields': (
            'nom', 'prenom', 'adresse',
            'telephone', 'profil', 'avatar', 'sexe',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'pseudo', 'nom', 'prenom', 'adresse',
                'telephone', 'profil', 'avatar', 'sexe', 'password'),
        }),
    )
    search_fields = ('pseudo', 'nom',)
    ordering = ('date_d_ajout',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)


class StationAdmin(admin.ModelAdmin):
    list_display = ('nom_de_la_station', 'responsable_de_la_station', 'contact_de_la_station',)
    list_filter = ('nom_de_la_station', 'responsable_de_la_station',)
    ordering = ('nom_de_la_station', 'responsable_de_la_station',)
    search_fields = ('nom_de_la_station', 'responsable_de_la_station',)


admin.site.register(Station, StationAdmin)


class ConducteurAdmin(admin.ModelAdmin):
    list_display = ('nom_et_prenom', 'age', 'niveau_etude', 'telephone', 'adresse', 'immatriculation',
                    'personne_a_prevenir', 'station', 'photo_passeport', 'numero_marie')
    list_filter = ('age', 'station', 'niveau_etude', 'immatriculation', 'personne_a_prevenir', 'numero_marie')
    ordering = ('age', 'station', 'niveau_etude', 'immatriculation', 'personne_a_prevenir', 'numero_marie')
    search_fields = ('age', 'station', 'niveau_etude', 'immatriculation', 'personne_a_prevenir', 'numero_marie')


admin.site.register(Conducteur, ConducteurAdmin)
