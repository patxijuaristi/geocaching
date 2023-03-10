from django.contrib import admin
from django.urls import path, include
from game.views import games_view, my_games_view, play_game_view, edit_game_view, delete_game, reset_game, create_game_view, my_game_detail_view, create_cache_view, found_cache, result_view

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
    path('games/<game_id>', play_game_view, name='play-game'),
    path('games/<game_id>/found-cache', found_cache, name='found-cache'),

    path('my-games', my_games_view, name='my-games'),
    path('my-games/create', create_game_view, name='create-game'),
    path('my-games/<game_id>', my_game_detail_view, name='my-game-detail'),
    path('my-games/<game_id>/new-cache', create_cache_view, name='new-cache'),
    path('my-games/<game_id>/result/<result_id>', result_view, name='result'),
    path('my-games/edit/<game_id>', edit_game_view, name='edit-game'),
    path('my-games/delete/<game_id>', delete_game, name='delete-game'),
    path('my-games/reset/<game_id>', reset_game, name='reset-game'),

    path('accounts/', include('allauth.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)