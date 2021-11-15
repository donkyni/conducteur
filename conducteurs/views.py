from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from conducteurs.forms import ConducteurForm, StationForm, UserUpdateForm, UserCreationForm, UserForm, ProfilsForm, \
    DroitsForm
from conducteurs.models import Conducteur, DroitsProfils, Droits, Profils, Station, User

@login_required
def controllers(request, url, droit, context):
    user_profil = request.user.profil
    dict = {}
    if user_profil:
        profils = get_object_or_404(Profils, nom=user_profil)
        droits = get_object_or_404(Droits, nom=droit)
        if profils:
            permissions = DroitsProfils.objects.filter(profil=profils, droit=droits)
            dict[profils] = permissions
            for permission in permissions:
                if permission.lecture:
                    print(permission)
                    return render(request, url, context)
                else:
                    return render(request, 'access_denied.html')


@login_required
def save_all(request, form, template_name, model, template_name2, mycontext):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            if model == "station":
                systeme = form.save(commit=False)
                systeme.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
            if model == "conducteur":
                systeme = form.save(commit=False)
                systeme.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
            if model == "utilisateur":
                systeme = form.save(commit=False)
                systeme.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
            if model == "profil":
                systeme = form.save(commit=False)
                systeme.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
            if model == "droit":
                systeme = form.save(commit=False)
                systeme.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
        else:
            data['form_is_valid'] = False

    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def index(request):
    stations = Station.objects.filter(archive=False)
    count_stations = Station.objects.filter(archive=False).count()
    conducteurs = Conducteur.objects.filter(archive=False)
    count_conducteurs = Conducteur.objects.filter(archive=False).count()
    form = ConducteurForm()
    context = {
        'form': form,
        'stations': stations,
        'count_stations': count_stations,
        'conducteurs': conducteurs,
        'count_conducteurs': count_conducteurs,
    }
    return render(request, 'index.html', context)


def addconducteur(request):
    conducteurs = Conducteur.objects.filter(archive=False)

    context = {'conducteurs': conducteurs}

    if request.method == 'POST':
        form = ConducteurForm(request.POST, request.FILES)
    else:
        form = ConducteurForm()

    return save_all(request, form, 'conducteur/addconducteur.html', 'conducteur',
                    'conducteur/listeconducteur.html', context)


@login_required
def ajouterconducteur(request):
    if request.method == 'POST':
        form = ConducteurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ajouterconducteur')
    else:
        form = ConducteurForm()

    station = Station.objects.filter(archive=False).count()
    conducteurs = Conducteur.objects.filter(archive=False).count()
    droitprofil = "Conducteur"
    current_date = datetime.now()

    context = {
        'form': form,
        'station': station,
        'conducteurs': conducteurs,
        'droitprofil': droitprofil,
        'current_date': current_date,
    }
    return controllers(request, 'conducteur/ajouterconducteur.html', droitprofil, locals())


@login_required
def modifierconducteur(request, id):
    conducteur = get_object_or_404(Conducteur, id=id)
    if request.method == 'POST':
        form = ConducteurForm(request.POST,
                              request.FILES,
                              instance=conducteur)
        if form.is_valid():
            form.save()
            messages.success(request, f'Vos informations ont été bien modifiés !')
            return redirect('modifierconducteur', conducteur.id)
    else:
        form = ConducteurForm(instance=conducteur)

    station = Station.objects.filter(archive=False).count()
    conducteurs = Conducteur.objects.filter(archive=False).count()
    droitprofil = "Conducteur"
    current_date = datetime.now()

    context = {
        'form': form
    }
    return controllers(request, 'conducteur/modifierconducteur.html', droitprofil, locals())


@login_required
def detailconducteur(request, id):
    conducteur = get_object_or_404(Conducteur, id=id)
    return render(request, 'conducteur/detailconducteur.html', locals())


def updateconducteur(request, id):
    conducteurs = Conducteur.objects.filter(archive=False)
    mycontext = {
        'conducteurs': conducteurs
    }
    conducteur = get_object_or_404(Conducteur, id=id)
    if request.method == 'POST':
        form = ConducteurForm(request.POST, request.FILES, instance=conducteur)
    else:
        form = ConducteurForm(instance=conducteur)
    return save_all(request, form, 'conducteur/updateconducteur.html', 'conducteur',
                    'conducteur/listeconducteur.html', mycontext)


@login_required
def deleteconducteur(request, id):
    data = dict()
    conducteur = get_object_or_404(Conducteur, id=id)
    if request.method == "POST":
        conducteur.archive = True
        conducteur.save()
        data['form_is_valid'] = True
        conducteurs = Conducteur.objects.filter(archive=False)
        data['conducteur'] = render_to_string('conducteur/listeconducteur.html', {'conducteurs': conducteurs})
    else:
        context = {
            'conducteur': conducteur,
        }
        data['html_form'] = render_to_string('conducteur/deleteconducteur.html', context, request=request)

    return JsonResponse(data)


def addstation(request):
    stations = Station.objects.filter(archive=False)

    context = {'stations': stations}

    if request.method == 'POST':
        form = StationForm(request.POST)
    else:
        form = StationForm()

    return save_all(request, form, 'station/addstation.html', 'station',
                    'station/listestation.html', context)


def updatestation(request, id):
    stations = Station.objects.filter(archive=False)
    mycontext = {
        'stations': stations
    }
    station = get_object_or_404(Station, id=id)
    if request.method == 'POST':
        form = StationForm(request.POST, instance=station)
    else:
        form = StationForm(instance=station)
    return save_all(request, form, 'station/updatestation.html', 'station',
                    'station/listestation.html', mycontext)


@login_required
def deletestation(request, id):
    data = dict()
    station = get_object_or_404(Station, id=id)
    if request.method == "POST":
        station.archive = True
        station.save()
        data['form_is_valid'] = True
        stations = Station.objects.filter(archive=False)
        data['station'] = render_to_string('station/listestation.html', {'stations': stations})
    else:
        context = {
            'station': station,
        }
        data['html_form'] = render_to_string('station/deletestation.html', context, request=request)

    return JsonResponse(data)


@login_required
def compte(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,
                                request.FILES,
                                instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Vos informations ont été bien modifiés !')
            redirect('compte')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
    }
    return render(request, 'parametre/compte.html', context)


@login_required
def utilisateurs(request):
    droitprofil = "Utilisateur"
    utilisateurs = User.objects.all()
    context = {
        'utilisateurs': utilisateurs
    }
    return controllers(request, 'parametre/utilisateurs.html', droitprofil, context)


def createutilisateur(request):
    utilisateurs = User.objects.all()
    mycontext = {
        'utilisateurs': utilisateurs
    }
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
    else:
        form = UserCreationForm()
    return save_all(request, form, 'parametre/createutilisateur.html',
                    'utilisateur', 'parametre/listutilisateur.html', mycontext)


def updateutilisateur(request, id):
    utilisateurs = User.objects.all()
    mycontext = {
        'utilisateurs': utilisateurs
    }
    utilisateur = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=utilisateur)
    else:
        form = UserForm(instance=utilisateur)
    return save_all(request, form, 'parametre/updateutilisateur.html',
                    'utilisateur', 'parametre/listutilisateur.html', mycontext)


@login_required
def deleteutilisateur(request, id):
    data = dict()
    utilisateur = get_object_or_404(User, id=id)
    if request.method == "POST":
        utilisateur.is_active = False
        utilisateur.save()
        data['form_is_valid'] = True
        utilisateurs = User.objects.all()
        data['utilisateur'] = render_to_string('parametre/listutilisateur.html',
                                               {'utilisateurs': utilisateurs})
    else:
        context = {
            'utilisateur': utilisateur
        }
        data['html_form'] = render_to_string('parametre/deleteutilisateur.html', context, request=request)

    return JsonResponse(data)


@login_required
def activeutilisateur(request, id):
    data = dict()
    utilisateur = get_object_or_404(User, id=id)
    if request.method == "POST":
        utilisateur.is_active = True
        utilisateur.save()
        data['form_is_valid'] = True
        utilisateurs = User.objects.all()
        data['utilisateur'] = render_to_string('parametre/listutilisateur.html',
                                               {'utilisateurs': utilisateurs})
    else:
        context = {
            'utilisateur': utilisateur
        }
        data['html_form'] = render_to_string('parametre/activeutilisateur.html', context, request=request)

    return JsonResponse(data)


@login_required
def profil(request):
    droitprofil = "Profil"
    profils = Profils.objects.filter(archive=False)
    context = {
        'profils': profils
    }
    return controllers(request, 'parametre/profil.html', droitprofil, context)


def createprofil(request):
    profils = Profils.objects.filter(archive=False)

    context = {'profils': profils}

    if request.method == 'POST':
        form = ProfilsForm(request.POST)
    else:
        form = ProfilsForm()

    return save_all(request, form, 'parametre/ajouterprofil.html', 'profil',
                    'parametre/listeprofil.html', context)


def updateprofil(request, id):
    profils = Profils.objects.filter(archive=False)
    mycontext = {
        'profils': profils
    }
    profil = get_object_or_404(Profils, id=id)
    if request.method == 'POST':
        form = ProfilsForm(request.POST, instance=profil)
    else:
        form = ProfilsForm(instance=profil)
    return save_all(request, form, 'parametre/updateprofil.html', 'profil',
                    'parametre/listeprofil.html', mycontext)


@login_required
def deleteprofil(request, id):
    data = dict()
    profil = get_object_or_404(Profils, id=id)
    if request.method == "POST":
        profil.archive = True
        profil.save()
        data['form_is_valid'] = True
        profils = Profils.objects.filter(archive=False)
        data['profil'] = render_to_string('parametre/listeprofil.html', {'profils': profils})
    else:
        context = {
            'profil': profil,
        }
        data['html_form'] = render_to_string('parametre/deleteprofil.html', context, request=request)

    return JsonResponse(data)


@login_required
def droit(request):
    droitprofil = "Droit"
    droits = Droits.objects.filter(archive=False)
    context = {
        'droits': droits
    }
    return controllers(request, 'parametre/droit.html', droitprofil, context)


def createdroit(request):
    droits = Droits.objects.filter(archive=False)

    context = {'droits': droits}

    if request.method == 'POST':
        form = DroitsForm(request.POST)
    else:
        form = DroitsForm()

    return save_all(request, form, 'parametre/ajouterdroit.html', 'droit',
                    'parametre/listedroit.html', context)


def updatedroit(request, id):
    droits = Droits.objects.filter(archive=False)
    mycontext = {
        'droit': droits
    }
    droit = get_object_or_404(Droits, id=id)
    if request.method == 'POST':
        form = DroitsForm(request.POST, instance=droit)
    else:
        form = DroitsForm(instance=droit)
    return save_all(request, form, 'parametre/updatedroit.html', 'droit',
                    'parametre/listedroit.html', mycontext)


@login_required
def deletedroit(request, id):
    data = dict()
    droit = get_object_or_404(Droits, id=id)
    if request.method == "POST":
        droit.archive = True
        droit.save()
        data['form_is_valid'] = True
        droits = Droits.objects.filter(archive=False)
        data['droit'] = render_to_string('parametre/listedroit.html', {'droits': droits})
    else:
        context = {
            'droit': droit,
        }
        data['html_form'] = render_to_string('parametre/deletedroit.html', context, request=request)

    return JsonResponse(data)
