from django.db import models

# Create your models here.


class T_users(models.Model):  # tabla<----- DB relacionada crudAjax
    nombre = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    edad = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre
