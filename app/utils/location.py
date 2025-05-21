import requests

def get_lat_lon_from_location(location_name):
    if not location_name:
        return None

    if location_name.strip().lower() in ["remote", "عن بعد", "remotely", "work from home"]:
        return None

    location_name = location_name.strip()
    if "palestine" not in location_name.lower():
        location_name += ", Palestine"
        
    url = "https://nominatim.openstreetmap.org/search"
    params = {'q': location_name, 'format': 'json'}
    headers = {'User-Agent': 'GivAndGrowGraduationProject/1.0'}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            return {
                "latitude": float(data[0]['lat']),
                "longitude": float(data[0]['lon'])
            }
        else:
            return None
    except requests.RequestException as e:
        return None
