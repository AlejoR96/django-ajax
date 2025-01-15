from django.db import models

# Create your models here.


class T_users(models.Model):
    nombre = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    edad = models.IntegerField(blank=True, null=True)
