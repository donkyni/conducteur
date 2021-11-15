from django.conf.urls import url

from conducteurs import views

urlpatterns = [
    url(r'^compte$', views.compte, name="compte"),
    url(r'^utilisateur$', views.utilisateurs, name="users"),
    url(r'^createutilisateur', views.createutilisateur, name='createutilisateur'),
    url(r'^(?P<id>\d+)/updateutilisateur', views.updateutilisateur, name="updateutilisateur"),
    url(r'^(?P<id>\d+)/deleteutilisateur', views.deleteutilisateur, name="deleteutilisateur"),
    url(r'^(?P<id>\d+)/activeutilisateur', views.activeutilisateur, name="activeutilisateur"),
    url(r'^profil', views.profil, name='profil'),
    url(r'^createprofil', views.createprofil, name='createprofil'),
    url(r'^(?P<id>\d+)/updateprofil', views.updateprofil, name="updateprofil"),
    url(r'^(?P<id>\d+)/deleteprofil', views.deleteprofil, name="deleteprofil"),
    url(r'^droit', views.droit, name='droit'),
    url(r'^createdroit', views.createdroit, name='createdroit'),
    url(r'^(?P<id>\d+)/updatedroit', views.updatedroit, name="updatedroit"),
    url(r'^(?P<id>\d+)/deletedroit', views.deletedroit, name="deletedroit"),
    url(r'^addconducteur$', views.addconducteur, name="addconducteur"),
    url(r'^ajouterconducteur$', views.ajouterconducteur, name="ajouterconducteur"),
    url(r'^(?P<id>\d+)/modifierconducteur', views.modifierconducteur, name="modifierconducteur"),
    url(r'^(?P<id>\d+)/detailconducteur', views.detailconducteur, name="detailconducteur"),
    url(r'^(?P<id>\d+)/updateconducteur', views.updateconducteur, name="updateconducteur"),
    url(r'^(?P<id>\d+)/deleteconducteur', views.deleteconducteur, name="deleteconducteur"),
    url(r'^addstation', views.addstation, name="addstation"),
    url(r'^(?P<id>\d+)/updatestation', views.updatestation, name="updatestation"),
    url(r'^(?P<id>\d+)/deletestation', views.deletestation, name="deletestation"),
]