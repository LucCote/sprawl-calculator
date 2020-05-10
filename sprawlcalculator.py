from PIL import Image
import requests
from io import BytesIO
import os

ZOOM_LEVEL = 10  # specifies how zoomed in satellite map image is (10x is slightly larger than a typical city)
SCALE_FACTOR = 100  # specifies how much to scale brightness/population score by (100 puts it in 1-2 digit range for typical city)

# mapbox api credentials
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoibHVjY2MiLCJhIjoiY2s5d2ZrYXhjMDRtZTNkbzZiYmNjM21ucyJ9.qZs4pcfb6Tn2i6xVwMpp8Q"
MAPBOX_MAP_STYLE = "/luccc/ck9x4eozb0lci1irpnz0qpnti"  # custom map style for high constrast between houses, roads, and nature

# geonames api credentials
GEONAMES_USERNAME = "luc_c"


def get_loc_img(longitude, latitude):
    # make a call to  mapbox api to get image centered on city's location
    img_data = requests.get("https://api.mapbox.com/styles/v1" + MAPBOX_MAP_STYLE + "/static/"
              + longitude + "," + latitude + "," + str(ZOOM_LEVEL)
              + ",0/400x400?access_token=" + MAPBOX_ACCESS_TOKEN)

    img_io = BytesIO()  # create output buffer to hold image
    img_io.write(img_data.content)  # write image to buffer
    city_img = Image.open(img_io)  # open image from buffer
    city_img = city_img.convert("L")  # convert to grayscale for ease of manipulation
    return city_img


def get_sprawl_score(img, population):
    total_bright = 0  # tracks number of bright(non-nature) pixels found

    # loop through image and find bright pixels
    for x in range(img.width):
        for y in range(img.height):
            if img.getpixel((x, y)) > 100:
                total_bright += 1
                img.putpixel((x, y), 255)  # set bright pixel to white (helps visualize what algorithm is finding)

    score = total_bright/int(population)*SCALE_FACTOR
    return score


def get_city_info(city):
    # make a call to geonames api to search for given city name
    info = requests.get("http://api.geonames.org/search?q=" + city + "&maxRows=1&type=json&username=" + GEONAMES_USERNAME).json()
    # check to ensure result exists and is a city
    if info['totalResultsCount'] == 0 or info['geonames'][0]['population'] == 0 or 'countryName' not in info['geonames'][0]:
        return

    # get relevant info from api result
    pop = info['geonames'][0]['population']
    lat = info['geonames'][0]['lat']
    long = info['geonames'][0]['lng']
    cntry = info['geonames'][0]['countryName']
    name = info['geonames'][0]['name']

    city_img = get_loc_img(long, lat)
    score = get_sprawl_score(city_img, pop)
    score = round(score, 2)  # score becomes hard to read/process at more than 2 decimal places

    return name, cntry, pop, lat, long, score, city_img
