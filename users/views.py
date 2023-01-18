from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth import  authenticate, login, logout
from django.contrib import messages

from .forms import UserLoginForm, UserRegisterForm

# Vista de login
def login_view(request):
    next = request.GET.get('next') # Se comprueba si hay una página siguiente y si la hay se coge
    form = UserLoginForm(request.POST or None) # Crea la clase de formulario de login
    if form.is_valid(): # Comprueba que el formulario es correcto
        username = form.cleaned_data.get('username') # recoge el campo de username del formulario
        password = form.cleaned_data.get('password') # recoge el campo de password del formulario
        user = authenticate(username=username, password=password) # autentica el usuario
        login(request, user) # realiza el login
        user.save() # guarda el usurio
        if next:
            return redirect(next) # si hay página siguiente la redirige ahí
        return redirect('/games') # sino la redirige a la página de mensajes
    else:
        if form.errors:
            messages.error(request, 'Wrong Credentials') # Si ocurre algun error durante el login lo incluye en messages para mostarlo en la vista

    context = {
        'form': form, # guarda el formulario en el contexto
    }
    
    return render(request, "login.html", context)


def signup_view(request):
    next = request.GET.get('next') # Se comprueba si hay una página siguiente y si la hay se coge
    form = UserRegisterForm(request.POST or None) # Crea la clase de formulario de registro
    if form.is_valid(): # Comprueba que el formulario es correcto
        user = form.save(commit=False) # Guarda el registro pero sin hacer commit en la BBDD
        password = form.cleaned_data.get('password') # Recoge la contresña
        user.set_password(password) # Se le aplica al usuario
        user.save() # Guarda el usuario en la BBDD
        login(request, user) # Realiza el login
        if next:
            return redirect(next) # si hay página siguiente la redirige ahí
        return redirect('/games') # sino la redirige a la página de mensajes
    else:
        for err in form.errors.values():
            messages.error(request, err) # Si ocurre algun error durante el registro lo incluye en messages para mostarlo en la vista

    context = {
        'form': form, # guarda el formulario en el contexto
    }
    return render(request, "signup.html", context)


def logout_view(request):
    logout(request) # Realiza el logout del usuario
    return redirect('/') # Redirige a la página de inicio