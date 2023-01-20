from django import forms
from .models import Cache, FoundCacheImage, Game

class GameCreationForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    picture = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'}), required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    zoom = forms.IntegerField(initial=10, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Game
        fields = [
            'name',
            'picture',
            'zoom',
        ]

class GameUpdateForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    picture = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'}), required=False)
    latitude = forms.DecimalField(max_digits=8, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    longitude = forms.DecimalField(max_digits=8, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    zoom = forms.IntegerField(initial=10, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Game
        fields = [
            'name',
            'picture',
            'latitude',
            'longitude',
            'zoom',
        ]

class CacheCreationForm(forms.ModelForm):

    hint = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    hint_picture = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'}), required=False)
    latitude = forms.DecimalField(max_digits=8, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    longitude = forms.DecimalField(max_digits=8, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    order = forms.IntegerField(initial=10, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Cache
        fields = [
            'hint',
            'hint_picture',
            'latitude',
            'longitude',
            'order',
        ]

class FoundCacheCreationForm(forms.ModelForm):

    cache_picture = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'}))

    class Meta:
        model = FoundCacheImage
        fields = [
            'cache_picture'
        ]