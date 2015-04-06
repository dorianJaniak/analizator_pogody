from django.db import models

# Create your models here.

class Stacja(models.Model):
    id=models.IntegerField(primary_key=True)
    nazwa=models.CharField(max_length=30)

class RodzajPomiaru(models.Model):
    id=models.IntegerField(primary_key=True)
    nazwa=models.CharField(max_length=20)


class DanePomiarowe(models.Model):
    id=models.IntegerField(primary_key=True)
    wartosc=models.IntegerField()
    rodzaj_pomiaru=models.ForeignKey(RodzajPomiaru, null=True)
    stacja=models.ForeignKey(Stacja, null=True)
    data=models.DateField()