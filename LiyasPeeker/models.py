from django.db import models


# Create your models here.
class Param_Societe(models.Model):
    raison_social = models.CharField(max_length=150,primary_key = True)
    activite = models.CharField(max_length=5000)
    ice_s = models.CharField(max_length=1000)
    if_s = models.CharField(max_length=1000)
    centre_rc = models.CharField(max_length=1000)
    num_rc = models.CharField(max_length=1000)
    capital = models.CharField(max_length=150)
    Forme_juridique = models.CharField(max_length=1000)
    date_creation = models.CharField(max_length=1000)
    effectif = models.CharField(max_length=1000)
    adresse = models.CharField(max_length=5000)
    Etat = models.CharField(max_length=1000)
    Tel = models.CharField(max_length=1000)
    Fax = models.CharField(max_length=1000)
    site_web = models.CharField(max_length=1000)
    Emails = models.CharField(max_length=3000)

    def __str__(self):
        return self.raison_social
