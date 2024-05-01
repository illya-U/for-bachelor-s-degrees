import folium
from django.shortcuts import render

# Create your views here.


def index(request):
    map = folium.Map()
    map.save("map/templates/map/footprint.html")
    return render(request, "map/footprint.html")

