from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from app.decorators import user_game_data
from .forms import GameCreationForm

from .models import Cache, Game, GameResult

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
def create_game_view(request):
    if request.method =='GET':
        form = GameCreationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, "game/create_game.html", context)
    else:
        form = GameCreationForm(request.POST, request.FILES or None)
        if form.is_valid():
            game = form.save(commit=False)
            game.creator = request.user
            game.save()
            messages.success(request, 'Game created correctly')
        return redirect('/my-games')

@login_required
@user_game_data
def edit_game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    if request.method =='GET':        
        form = GameCreationForm(request.POST or None, instance=game)
        context = {
            'form': form,
            'update': True
        }
        return render(request, "game/create_game.html", context)
    else:
        form = GameCreationForm(request.POST, request.FILES or None, instance=game)
        if form.is_valid():
            form.save()
        return redirect('/my-games')

@login_required
@user_game_data
def delete_game(request, game_id):
    try:
        game = get_object_or_404(Game, id=game_id)
        game.picture.delete()
        game.delete()
        messages.success(request, 'Game removed correctly')
    except:
        messages.error(request, 'It was not possible to remove this game')
        pass
    
    
    return redirect('my-games')

@login_required
@user_game_data
def reset_game(request, game_id):
    try:
        game = get_object_or_404(Game, id=game_id)
        results = GameResult.objects.filter(game=game)
        results.delete()
        game.winner = None
        game.active = True
        game.save()
        messages.success(request, 'Game reseted correctly')
    except:
        messages.error(request, 'It was not possible to remove this question')
        pass
    
    
    return redirect('my-games')
