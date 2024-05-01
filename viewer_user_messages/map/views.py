import folium
from django.shortcuts import render
from .models import PointOnTheMap

# Create your views here.
START_POINT = [50, 30]


def index(request):
    map = folium.Map(START_POINT, zoom_start=6)
    points = PointOnTheMap.objects.all()
    for point in points:
        marker = folium.Marker([point.latitude, point.longitude], popup=point.message)
        marker.add_to(map)
    map.save("map/templates/map/footprint.html")
    return render(request, "map/footprint.html")

