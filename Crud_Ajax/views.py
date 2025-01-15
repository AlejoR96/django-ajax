from django.shortcuts import render
from django.views.generic import ListView
from .models import T_users

# Create your views here.


class crudView(ListView):
    model: T_users
    template_name = 'crud_ajax/crud.html'
    context_object_name = 'users'
