from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from game.models import Cache, Game

@login_required
def games_view(request):
    games = Game.objects.all()
    
    context = {
        'games': games,
    }
    return render(request, "game/game_list.html", context)


@login_required
def my_games_view(request):
    games = Game.objects.filter(creator=request.user)
    
    context = {
        'games': games,
    }
    return render(request, "game/my_games.html", context)

@login_required
def play_game_view(request, game_id):
    games = Game.objects.filter(creator=request.user)
    
    context = {
        'games': games,
    }
    return render(request, "game/play_game.html", context)

@login_required
def edit_game_view(request, game_id):
    games = Game.objects.filter(creator=request.user)
    
    context = {
        'games': games,
    }
    return render(request, "game/create_game.html", context)