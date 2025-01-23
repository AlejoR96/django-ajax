from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView, View
from .models import T_users

# Create your views here.


class crudView(ListView):  # Vista para listar los usuarios creados en la DB
    model = T_users
    template_name = 'crud_ajax/crud.html'
    context_object_name = 'users'

    def post(self, request, *args, **kwargs):
        # Capturar los datos enviados en la solicitud POST
        try:
            nombre = request.POST.get('name')
            direccion = request.POST.get('direccion')
            edad = request.POST.get('edad')

            # Crear un nuevo usuario
            if nombre and direccion and edad:
                new_user = T_users(
                    nombre=nombre,
                    direccion=direccion,
                    edad=edad,
                )
                new_user.save()

            # Mensaje de éxito (puedes guardarlo en la sesión si es necesario)
            request.session['success_message'] = f"El usuario {
                nombre} ha sido creado exitosamente."
        except Exception as e:
            # Mensaje de error
            request.session['error_message'] = f"Ocurrió un error: {str(e)}"

        # Redirigir a la misma página (evita el reenvío del formulario)
        return redirect(reverse('crud'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Extraer mensajes de la sesión
        context['success_message'] = self.request.session.pop(
            'success_message', None)
        context['error_message'] = self.request.session.pop(
            'error_message', None)
        return context


class createUser(View):
    def get(self, request):
        print(request)
        nom_usario = request.GET.get('nombre', None)
        dire_usario = request.GET.get('direccion', None)
        edad_usario = request.GET.get('edad', None)

        obj = T_users.objects.create(
            nombre=nom_usario,
            direccion=dire_usario,
            edad=edad_usario
        )
        usuario = {'id': obj.id, 'nombre': obj.nombre,
                   'direccion': obj.direccion, 'edad': obj.edad}

        data = {
            'usuario': usuario
        }

        return JsonResponse(data)


class EditCrudUser(View):
    def post(self, request, *args, **kwargs):
        response_data = {'updated': False}  # Valor por defecto
        id = request.POST.get('id', None)
        nombre = request.POST.get('nombre', None)
        direccion = request.POST.get('direccion', None)
        edad = request.POST.get('edad', None)

        if id and nombre and direccion and edad:
            try:
                # Intentar obtener el usuario
                user = T_users.objects.get(id=id)

                # Actualizar los campos
                user.nombre = nombre
                user.direccion = direccion
                user.edad = edad
                user.save()

                response_data['updated'] = True
            except T_users.DoesNotExist:
                response_data['error'] = f"No se encontró el usuario con ID {
                    id}."
            except Exception as e:
                response_data['error'] = f"Error inesperado: {str(e)}"
        else:
            response_data['error'] = "Todos los campos son obligatorios."

        return JsonResponse(response_data)


class DeleteCrudUser(View):
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        response_data = {'deleted': False}  # Valor por defecto

        if id:
            try:
                # Intentar eliminar el registro
                user = T_users.objects.get(id=id)
                user.delete()
                response_data['deleted'] = True
            except T_users.DoesNotExist:
                # Si no existe el registro, informar
                response_data['error'] = f"No se encontró el usuario con ID {
                    id}."
            except Exception as e:
                # Manejo de errores generales
                response_data['error'] = f"Error inesperado: {str(e)}"
        else:
            response_data['error'] = "No se proporcionó un ID válido."

        return JsonResponse(response_data)
