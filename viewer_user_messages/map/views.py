import folium
from django.template.loader import render_to_string
from django.views.generic import TemplateView


from .models import PointOnTheMap, User

# Create your views here.
START_POINT = [50, 30]
photo_path = "http://127.0.0.1:8000/static/"


class MapView(TemplateView):
    template_name = 'map/map.html'

    def get_context_data(self, **kwargs):
        figure = folium.Figure()

        # Make the map
        map = folium.Map(location=START_POINT, zoom_start=6)

        map.add_to(figure)

        points = PointOnTheMap.objects.all()

        for point in points:

            user = User.objects.using("default").get(user_id=point.user_id)

            context = {
                "user_photo_url": photo_path + str(user.user_photo_path),
                "user_name": user.user_name,
                "message": point.message,
                "location_photo": photo_path + str(point.photo_path),
            }
            html = render_to_string("map/popup.html", {"context": context})
            iframe = folium.IFrame(html=html, width=400, height=700)
            popup = folium.Popup(iframe, max_width=1000)
            marker = folium.Marker([point.latitude, point.longitude], popup=popup)
            marker.add_to(map)

        # Render and send to template
        figure.render()
        return {"map": figure}


