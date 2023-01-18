from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from game.models import Cache, Game

@login_required
def games_view(request):
    game = get_object_or_404(Game, name='Malaga Geo')
    print(game)
    try:
        cache = Cache.objects.filter(game=game).get(order=7)
        print(cache)
    except ObjectDoesNotExist:
        print('siiiiiiiii')
    
    return redirect('/')


@login_required
def my_games_view(request):
    return redirect('/')