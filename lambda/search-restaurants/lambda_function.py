import json
import math
import urllib.request
import urllib.parse


OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two geographic coordinates
    using the Haversine formula.
    """

    earth_radius_km = 6371

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius_km * c


def build_overpass_query(latitude, longitude, radius, cuisine):
    """
    Builds the Overpass API query.
    """

    if cuisine and cuisine.lower() != "any":
        cuisine_filter = f'[cuisine="{cuisine}"]'
    else:
        cuisine_filter = ""

    return f"""
    [out:json];

    (
        node[
            "amenity"="restaurant"
            {cuisine_filter}
        ](
            around:{radius},
            {latitude},
            {longitude}
        );

        way[
            "amenity"="restaurant"
            {cuisine_filter}
        ](
            around:{radius},
            {latitude},
            {longitude}
        );
    );

    out center;
    """


def query_overpass(query):
    """
    Sends the query to the Overpass API.
    """

    data = urllib.parse.urlencode({
        "data": query
    }).encode("utf-8")

    request = urllib.request.Request(
        OVERPASS_URL,
        data=data,
        headers={
            "User-Agent": "delivery-ai-assistant/1.0"
        }
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def extract_restaurants(data, user_latitude, user_longitude):
    """
    Converts OpenStreetMap results into a simplified structure.
    """

    restaurants = []

    for element in data.get("elements", []):

        tags = element.get("tags", {})

        latitude = element.get("lat")
        longitude = element.get("lon")

        # Ways usually contain their coordinates inside "center".
        if latitude is None:

            center = element.get("center", {})

            latitude = center.get("lat")
            longitude = center.get("lon")

        if latitude is None or longitude is None:
            continue

        distance = calculate_distance(
            user_latitude,
            user_longitude,
            latitude,
            longitude
        )

        restaurant = {
            "name": tags.get(
                "name",
                "Restaurant without name"
            ),

            "cuisine": tags.get(
                "cuisine",
                "Not informed"
            ),

            "address": tags.get(
                "addr:street",
                "Address not informed"
            ),

            "phone": tags.get("phone"),

            "website": tags.get("website"),

            "latitude": latitude,

            "longitude": longitude,

            "distance_km": round(distance, 2)
        }

        restaurants.append(restaurant)

    # Closest restaurants first.
    restaurants.sort(
        key=lambda restaurant: restaurant["distance_km"]
    )

    return restaurants


def lambda_handler(event, context):

    latitude = float(event["latitude"])
    longitude = float(event["longitude"])

    radius = int(
        event.get("radius_m", 5000)
    )

    cuisine = event.get(
        "cuisine",
        "any"
    )

    quantity = int(
        event.get("quantity", 20)
    )

    query = build_overpass_query(
        latitude,
        longitude,
        radius,
        cuisine
    )

    data = query_overpass(query)

    restaurants = extract_restaurants(
        data,
        latitude,
        longitude
    )

    restaurants = restaurants[:quantity]

    return {
        "status": "success",

        "source": "OpenStreetMap / Overpass API",

        "search": {
            "latitude": latitude,
            "longitude": longitude,
            "radius_m": radius,
            "cuisine": cuisine
        },

        "count": len(restaurants),

        "restaurants": restaurants
    }
