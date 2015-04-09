from django.db import models
from datetime import datetime

# Create your models here.

class Stacja(models.Model):
    id = models.IntegerField(primary_key=True)
    nazwa = models.CharField(max_length=30)

    def __str__(self):
        return self.nazwa

class Jednostka(models.Model):
    id = models.IntegerField(primary_key=True)
    nazwa = models.CharField(max_length=20)

    def __str__(self):
        return self.nazwa

class RodzajPomiaru(models.Model):
    id = models.IntegerField(primary_key=True)
    nazwa = models.CharField(max_length=20)
    jednostka = models.ForeignKey(Jednostka,null=True)

    def __str__(self):
        return self.nazwa


class DanePomiarowe(models.Model):
    id = models.IntegerField(primary_key=True)
    wartosc = models.IntegerField()
    rodzaj_pomiaru = models.ForeignKey(RodzajPomiaru, null=True)
    stacja = models.ForeignKey(Stacja, null=True)
    data = models.DateTimeField(default=datetime.now(), null=True)

    def __str__(self):
        return "%s [%s] @ %s" % (self.wartosc, self.rodzaj_pomiaru, self.stacja)