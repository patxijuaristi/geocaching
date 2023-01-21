from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.decorators import user_game_data
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .utils import create_map
from .forms import FoundCacheCreationForm, GameCreationForm, CacheCreationForm, GameUpdateForm
from .models import Cache, Game, GameResult

import geocoder

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

    try:
        GameResult.objects.filter(game=game).get(player=request.user)
    except ObjectDoesNotExist:
        GameResult.objects.create(game=game, player=request.user)
        pass

    found_form = FoundCacheCreationForm(request.POST or None)

    folium_map = create_map(game, request.user, True)

    context = {
        'map': folium_map,
        'game': game,
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
    partidas = game.game_result.all()

    folium_map = create_map(game, request.user, False)

    context = {
        'map': folium_map,
        'game': game,
        'partidas': partidas
    }
    return render(request, "game/my_game_detail.html", context)

@login_required
@user_game_data
def result_view(request, game_id, result_id):
    game = get_object_or_404(Game, id=game_id)
    result = game.game_result.get(id=result_id)
    found_cache_imgs = result.found_cache.all()

    context = {
        'result': result,
        'found_cache_imgs': found_cache_imgs,
        'game': game,
    }
    return render(request, "game/result_detail.html", context)

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
            location = geocoder.osm(form.cleaned_data.get('address'))
            game.latitude = location.lat
            game.longitude = location.lng
            game.creator = request.user
            game.save()
            messages.success(request, 'Game created correctly')
        return redirect('/my-games')

@login_required
@user_game_data
def edit_game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    if request.method =='GET':        
        form = GameUpdateForm(request.POST or None, instance=game)
        context = {
            'form': form,
            'update': True,
            'game_id': game_id
        }
        return render(request, "game/create_game.html", context)
    else:
        form = GameUpdateForm(request.POST, request.FILES or None, instance=game)
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
        try:
            form = CacheCreationForm(request.POST, request.FILES or None)
            if form.is_valid():
                cache = form.save(commit=False)
                game = get_object_or_404(Game, id=game_id)
                cache.game = game
                cache.save()
                messages.success(request, 'Game created correctly')
            else:
                messages.error(request, form.errors)
        except ValidationError:
            messages.error(request, 'You need to change the order of the cache with this order. Or change the order of this cache')
            return redirect('/my-games/'+ str(game_id) +'/new-cache')


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
