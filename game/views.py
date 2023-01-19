from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from app.decorators import user_game_data
from .forms import FoundCacheCreationForm, GameCreationForm, CacheCreationForm
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Cache, Game, GameResult
import folium

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
    game = get_object_or_404(Game, id=game_id)
    caches = game.game_cache.all()

    try:
        GameResult.objects.filter(game=game).get(player=request.user)
    except ObjectDoesNotExist:
        GameResult.objects.create(game=game, player=request.user)
        pass

    found_form = FoundCacheCreationForm(request.POST or None)

    start_coords = (game.latitude, game.longitude)
    folium_map = folium.Map(location=start_coords,
                            zoom_start=game.radius,
                            attr="https://www.openstreetmap.org/#map=6/40.007/-2.488",
                            max_zoom=18,
                            min_zoom=15,
                            )

    mymap = folium_map._repr_html_()  # HTML representation of the map

    context = {
        'map': mymap,
        'game': game,
        'caches': caches,
        'found_form': found_form,
        'game_id': game_id
    }
    return render(request, "game/play_game.html", context)

@login_required
def found_cache(request, game_id):
    form = FoundCacheCreationForm(request.POST, request.FILES or None)
    if form.is_valid():
        f_img = form.save(commit=False)
        game = get_object_or_404(Game, id=game_id)
        game_result = GameResult.objects.filter(game=game).get(player=request.user)
        game_result.found_caches = game_result.found_caches + 1
        game_result.save()

        f_img.game_result = game_result
        f_img.save()

        total_caches = game.game_cache.all().count()
        if total_caches == game_result.found_caches:
            game.active = False
            game.winner = request.user
            game.save()
        messages.success(request, 'Cache finding added correctly')
    return redirect('/games/' + str(game_id))

@login_required
@user_game_data
def my_game_detail_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    caches = game.game_cache.all()
    partidas = game.game_result.all()

    start_coords = (game.latitude, game.longitude)
    folium_map = folium.Map(location=start_coords,
                            zoom_start=game.radius,
                            attr="https://www.openstreetmap.org/#map=6/40.007/-2.488",
                            max_zoom=18,
                            min_zoom=15,
                            )

    mymap = folium_map._repr_html_()  # HTML representation of the map
    
    context = {
        'map': mymap,
        'game': game,
        'caches': caches,
        'partidas': partidas
    }
    return render(request, "game/my_game_detail.html", context)

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
            'update': True,
            'game_id': game_id
        }
        return render(request, "game/create_game.html", context)
    else:
        form = GameCreationForm(request.POST, request.FILES or None, instance=game)
        if form.is_valid():
            form.save()
        return redirect('/my-games')

@login_required
def create_cache_view(request, game_id):
    if request.method =='GET':
        form = CacheCreationForm(request.POST or None)
        context = {
            'form': form,
            'game_id': game_id
        }
        return render(request, "game/create_cache.html", context)
    else:
        form = CacheCreationForm(request.POST, request.FILES or None)
        if form.is_valid():
            cache = form.save(commit=False)
            game = get_object_or_404(Game, id=game_id)
            cache.game = game
            cache.save()
            messages.success(request, 'Game created correctly')
        return redirect('/my-games')

@login_required
@user_game_data
def edit_cache_view(request, game_id, cache_id):
    cache = get_object_or_404(Cache, id=cache_id)
    
    if request.method =='GET':        
        form = CacheCreationForm(request.POST or None, instance=cache)
        context = {
            'form': form,
            'update': True,
            'game_id': game_id
        }
        return render(request, "game/create_cache.html", context)
    else:
        form = CacheCreationForm(request.POST, request.FILES or None, instance=cache)
        if form.is_valid():
            form.save()
        return redirect('/my-games/' + str(game_id))

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
