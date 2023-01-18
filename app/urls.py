from django.contrib import admin
from django.urls import path
from game.views import games_view, my_games_view

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
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)