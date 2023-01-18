import functools
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib import messages

from game.models import Game

def user_game_data(view_func):
    """
        this decorator ensures that a user is not logged in,
        if a user is logged in, the user will get redirected to 
        the url whose view name was passed to the redirect_url parameter
    """
    @functools.wraps(view_func)
    def wrapper(request, game_id, *args, **kwargs):
        print(request.user)
        print(game_id)
        game = get_object_or_404(Game, id=game_id)
        if game.creator != request.user:
            return HttpResponseForbidden()
        return view_func(request, game_id, *args, **kwargs)
    return wrapper