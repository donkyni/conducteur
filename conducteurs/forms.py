from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from conducteurs.models import User, Profils, Droits, Conducteur, Station


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'pseudo', 'nom', 'prenom', 'adresse', 'telephone', 'profil', 'avatar', 'sexe')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'pseudo', 'nom', 'prenom', 'adresse', 'telephone', 'profil', 'avatar', 'sexe')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'nom', 'prenom', 'adresse', 'telephone', 'sexe', 'avatar'
        )


class ProfilsForm(forms.ModelForm):
    class Meta:
        model = Profils
        fields = ('nom',)
        labels = {
            'nom': _('Nom du profil')
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'})
        }


class DroitsForm(forms.ModelForm):
    class Meta:
        model = Droits
        fields = ('nom',)
        labels = {
            'nom': _('Nom du droit')
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'})
        }


class ConducteurForm(forms.ModelForm):
    class Meta:
        model = Conducteur
        exclude = ('archive',)
        labels = {
            'nom_et_prenom': _('Nom et prénom')
        }
        widgets = {
            'niveau_etude': forms.Select(attrs={'class': 'form-control', 'data-live-search': 'true'}),
            'station': forms.Select(attrs={'class': 'form-control', 'data-live-search': 'true'}),
            'nom_et_prenom': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 15}),
            'immatriculation': forms.TextInput(attrs={'class': 'form-control'}),
            'personne_a_prevenir': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 15}),
        }


class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        exclude = ('archive',)
        labels = {
            'nom_de_la_station': _('Station')
        }
