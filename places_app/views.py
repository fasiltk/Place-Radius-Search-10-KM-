from django.shortcuts import render
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .models import Place

# ---------------------------
# Add Place (Auto geocode)
# ---------------------------
def add_place(request):
    if request.method == "POST":
        place_name = request.POST.get("place_name")

        geolocator = Nominatim(user_agent="places_project")
        location = geolocator.geocode(place_name)

        if not location:
            return render(request, "add_place.html", {
                "error": "Location not found, try again!"
            })

        # Save to DB
        Place.objects.create(
            name=place_name,
            latitude=location.latitude,
            longitude=location.longitude
        )

        return render(request, "add_place.html", {
            "success": f"{place_name} added successfully!"
        })

    return render(request, "add_place.html")


# ---------------------------
# Find places within 10 KM
# ---------------------------
def search_nearby(request):
    if request.method == "POST":
        input_name = request.POST.get("place_name")

        geolocator = Nominatim(user_agent="places_project")
        location = geolocator.geocode(input_name)

        if not location:
            return render(request, "search.html", {
                "error": "Place not found!"
            })

        input_coords = (location.latitude, location.longitude)
        nearby = []

        for place in Place.objects.all():
            dist = geodesic(
                input_coords,
                (place.latitude, place.longitude)
            ).km

            if dist <= 10:
                nearby.append({
                    "name": place.name,
                    "distance": round(dist, 2)
                })

        return render(request, "results.html", {
            "search_input": input_name,
            "places": nearby
        })

    return render(request, "search.html")
