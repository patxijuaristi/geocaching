from django.contrib import admin
from django.urls import path
from game.views import games_view, my_games_view, play_game_view, edit_game_view, delete_game, reset_game

from home.views import home_view
from users.views import login_view, signup_view, logout_view

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin', admin.site.urls),
    path('', home_view, name='home'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('register', signup_view, name='signup'),
    path('games', games_view, name='games'),
    path('my-games', my_games_view, name='my-games'),
    path('games/<game_id>', play_game_view, name='play-game'),
    path('my-games/<game_id>', edit_game_view, name='edit-game'),
    path('my-games/delete/<game_id>', delete_game, name='delete-game'),
    path('my-games/reset/<game_id>', reset_game, name='delete-game'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)