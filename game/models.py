from django.db import models

from users.models import User

class Game(models.Model):

    name = models.CharField(max_length=200)
    picture = models.ImageField()
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_creator')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_winner')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Cache(models.Model):

    class Meta:
        ordering = ['order']
    
    hint = models.CharField(max_length=200)
    hint_picture = models.ImageField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    order = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_cache')

    def __str__(self):
        return self.hint + ' - Game: ' + self.game.name

class GameResult(models.Model):
    
    found_caches = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_result')
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_player')

    def __str__(self):
        return self.player + ' found ' + self.found_caches + ' caches in game: ' + self.game.name