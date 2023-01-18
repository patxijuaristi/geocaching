from django.contrib import admin

from .models import Cache, Game, GameResult

class CustomGame(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude", "radius", "creator", "active")

class CustomCache(admin.ModelAdmin):
    list_display = ("hint", "hint_picture", "latitude", "longitude", "order", "game")

class CustomGameResult(admin.ModelAdmin):
    list_display = ("player", "game", "found_caches")


admin.site.register(Game, CustomGame)
admin.site.register(Cache, CustomCache)
admin.site.register(GameResult, CustomGameResult)