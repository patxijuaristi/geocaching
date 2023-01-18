from django import forms
from .models import Game

class GameCreationForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    picture = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'}), required=False)
    latitude = forms.DecimalField(max_digits=8, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    longitude = forms.DecimalField(max_digits=8, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    radius = forms.IntegerField(initial=10, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Game
        fields = [
            'name',
            'picture',
            'latitude',
            'longitude',
            'radius',
        ]