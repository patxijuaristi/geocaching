from django.shortcuts import render

#Vista de la home
def home_view(request):
    return render(request, "home.html")

