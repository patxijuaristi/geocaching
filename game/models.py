from django.db import models
from django.shortcuts import get_object_or_404

from users.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist

class Game(models.Model):

    name = models.CharField(max_length=200)
    picture = models.ImageField(null=True, blank=True, upload_to='game/')
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_creator')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_winner', null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Cache(models.Model):

    class Meta:
        ordering = ['order']
    
    hint = models.CharField(max_length=200, null=True, blank=True)
    hint_picture = models.ImageField(null=True, blank=True, upload_to='cache/')
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    order = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_cache')

    def __str__(self):
        if(self.hint):
            return self.hint + ' - Game: ' + self.game.name
        return self.hint_picture.name + ' - Game: ' + self.game.name
    
    def clean(self):
        if self.hint == None and self.hint_picture == None:
            raise ValidationError('You need to specify a hint or a picture.')
        
        '''try:
            Cache.objects.filter(game=self.game).get(order=self.order)
            raise ValidationError('You need to change the order of the cache with this order. Or change the order of this cache')
        except ObjectDoesNotExist:
            pass'''
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

class GameResult(models.Model):
    
    found_caches = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_result')
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_player')

    def __str__(self):
        return self.player.email + ' found ' + str(self.found_caches) + ' caches in game: ' + self.game.name

class FoundCacheImage(models.Model):
    
    cache_picture = models.ImageField(default='test.png',  upload_to='found-cache/')
    game_result = models.ForeignKey(GameResult, on_delete=models.CASCADE, related_name='found_cache')