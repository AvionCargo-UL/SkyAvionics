import requests
from PIL import Image
from io import BytesIO


def get_static_map(api_key, lat, lon, zoom=15, size='1000x1000', map_type='satellite'):
    # Construct the Static Map URL with satellite view
    url = (
        f"https://maps.googleapis.com/maps/api/staticmap?"
        f"center={lat},{lon}&zoom={zoom}&size={size}&maptype={map_type}&key={api_key}"
    )

    # Get the image
    response = requests.get(url)

    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print(f"Error: {response.status_code}")
        return None


def calculate_bounding_box(lat, lon, width, height, zoom):
    # This calculation assumes a simple projection and may vary based on zoom level and location
    lat_offset = (height / 256) * (360 / (2 ** zoom))
    lon_offset = (width / 256) * (360 / (2 ** zoom)) / (lat * 3.14159 / 180)

    top_left_lat = lat + lat_offset / 2
    top_left_lon = lon - lon_offset / 2
    bottom_right_lat = lat - lat_offset / 2
    bottom_right_lon = lon + lon_offset / 2

    return (top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon)


def main():
    API_KEY = 'AIzaSyBVWLTfNjXZdzS7E9ICvreJuvVGjVEWt9k'
    latitude = 32.610013 # Example latitude
    longitude = -97.484008  # Example longitude
    zoom = 18
    width = 800
    height = 800

    # Get the static map image
    map_image = get_static_map(API_KEY, latitude, longitude, zoom=zoom, size=f"{width}x{height}")

    if map_image:
        map_image.show()  # Display the image

        # Calculate the bounding box
        bounding_box = calculate_bounding_box(latitude, longitude, width, height, zoom)
        print(f"Top-left (Lat, Lon): {bounding_box[0]}, {bounding_box[1]}")
        print(f"Bottom-right (Lat, Lon): {bounding_box[2]}, {bounding_box[3]}")

if __name__ == "__main__":
    main()