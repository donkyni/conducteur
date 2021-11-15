from django.db import models
from django.contrib.auth import models as auth_models


class Droits(models.Model):
    nom = models.CharField(max_length=255)
    archive = models.BooleanField(default=False, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ('-id',)
        verbose_name = "Droits"
        verbose_name_plural = "Droits"


class Profils(models.Model):
    nom = models.CharField(max_length=255, null=True)
    droits = models.ManyToManyField(Droits, through="DroitsProfils")
    archive = models.BooleanField(default=False, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ('-id',)
        verbose_name = "Profil"
        verbose_name_plural = "Profil"


class DroitsProfils(models.Model):
    profil = models.ForeignKey(Profils, on_delete=models.SET_NULL, null=True)
    droit = models.ForeignKey(Droits, on_delete=models.SET_NULL, null=True)
    ecriture = models.BooleanField(default=False, null=True)
    lecture = models.BooleanField(default=False, null=True)
    modification = models.BooleanField(default=False, null=True)
    suppression = models.BooleanField(default=False, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = "Droits profils"
        verbose_name_plural = "Droits profils"


class UserManager(auth_models.BaseUserManager):

    def create_user(self, pseudo, adresse, nom, prenom, password=None):
        if not pseudo:
            raise ValueError('Users must have an telephone number')
        user = self.model(pseudo=pseudo)
        user.adresse = adresse
        user.nom = nom
        user.prenom = prenom
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, pseudo, adresse, nom, prenom, password):
        user = self.create_user(
            pseudo,
            adresse=adresse,
            nom=nom,
            prenom=prenom,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    SEXE = (
        (u"Homme", u"Homme"),
        (u"Femme", u"Femme")
    )

    """
    Informations de base
    """
    pseudo = models.CharField(unique=True, max_length=255, null=True, blank=False,
                              help_text="Le nom d'utilisateur servira à se connecter à la plateforme")
    nom = models.CharField(max_length=255, null=True)
    prenom = models.CharField(max_length=255, blank=False, null=True)
    adresse = models.CharField(max_length=255, null=True, blank=False)
    telephone = models.BigIntegerField(blank=False, null=True, unique=True)
    profil = models.ForeignKey(Profils, on_delete=models.SET_NULL, null=True)

    """
    Informations supplémentaires
    """
    avatar = models.ImageField(blank=True, null=True, upload_to="avatars")
    sexe = models.CharField(choices=SEXE, max_length=120, null=True, blank=True, )

    """
    Données systèmes
    """

    """
    Django settings
    """
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_d_ajout = models.DateTimeField(auto_now_add=True, null=True,
                                        verbose_name="Date d'enrégistrement de l'utilisateur")

    objects = UserManager()

    USERNAME_FIELD = 'pseudo'
    REQUIRED_FIELDS = ['nom', 'prenom', 'adresse']

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateur'
        ordering = ('-id',)

    def __str__(self):
        return self.nom + ' ' + self.prenom

    def has_perm(self, perm, obj=None):
        """Does the utilisateur have a specific permission?"""
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        """Does the utilisateur have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return self.is_admin

    @property
    def is_staff(self):
        """Is the utilisateur a member of staff?"""
        # Réponse la plus simple possible : Tous les administrateurs sont du personnel
        return self.is_active

    def __unicode__(self):
        # pass
        return u'{0}'.format(self.get_full_name())

    def get_short_name(self):
        # pass
        return self.nom

    def get_full_name(self):
        # pass
        return u'{0} {1}'.format(self.nom, self.prenom)


class Station(models.Model):
    nom_de_la_station = models.CharField(max_length=255, null=True)
    responsable_de_la_station = models.CharField(max_length=255, null=True)
    contact_de_la_station = models.CharField(max_length=255, null=True)
    archive = models.BooleanField(default=False, null=True)

    def __str__(self): return self.nom_de_la_station


class Conducteur(models.Model):
    NIVEAU = (
        (u"Secondaire sans diplôme", u"Secondaire sans diplôme"),
        (u"Secondaire avec diplôme", u"Secondaire avec diplôme"),
        (u"Primaire sans diplôme", u"Primaire sans diplôme"),
        (u"Primaire avec diplôme", u"Primaire avec diplôme"),
        (u"Lycée sans diplôme", u"Lycée sans diplôme"),
        (u"Lycée avec diplôme", u"Lycée avec diplôme"),
    )
    nom_et_prenom = models.TextField(null=True)
    age = models.IntegerField(null=True)
    niveau_etude = models.CharField(choices=NIVEAU, max_length=255, null=True)
    telephone = models.CharField(max_length=255, null=True)
    adresse = models.CharField(max_length=255, null=True)
    immatriculation = models.TextField(null=True)
    personne_a_prevenir = models.TextField(null=True)
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)
    photo_passeport = models.ImageField(null=True, upload_to="photo_passeport", blank=True)
    numero_marie = models.CharField(max_length=20, null=True)
    archive = models.BooleanField(default=False, null=True)

    def __str__(self): return self.nom_et_prenom
