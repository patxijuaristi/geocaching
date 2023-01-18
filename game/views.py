from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def games_view(request):
    return redirect('/')


@login_required
def my_games_view(request):
    return redirect('/')