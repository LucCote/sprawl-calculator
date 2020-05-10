from flask import Flask, request, jsonify, send_file
import sprawlcalculator as sc
from io import BytesIO

app = Flask(__name__)  # Initialize Flask

# default call to server, returns json object containing city name, country, population, latitude, longitude, and sprawl score
@app.route('/', methods=['GET'])
def default():
    city = request.args.get('city')
    result = sc.get_city_info(city)
    data = {}
    if result:  # add all relevant info to data dictionary
        name, cntry, pop, lat, long, sprawl_score, city_img = result
        data['city_name'] = name
        data['country'] = cntry
        data['population'] = pop
        data['latitude'] = lat
        data['longitude'] = long
        data['sprawl_score'] = sprawl_score
    return jsonify(data)  # convert dictionary to json object and serve

# call to server/image, returns jpeg file of image of city with pixels of interest highlighted (roads and mid-high density housing)
@app.route('/image', methods=['GET'])
def image():
    city = request.args.get('city')
    result = sc.get_city_info(city)
    if result:
        name, cntry, pop, lat, long, sprawl_score, city_img = result
        img_io = BytesIO()  # create output buffer to hold image
        city_img.save(img_io, 'JPEG')  # write image to output buffer
        img_io.seek(0)  # set buffer pointer to start of buffer
        return send_file(img_io, mimetype='image/jpeg')  # serve image written to buffer
    return "failed"
