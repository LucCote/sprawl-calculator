# sprawl-calculator
An API which takes a city name and uses information from Mapbox and Geoname APIs in order to calculate a score for how sprawled said city is

### Calculation
The sprawl-calculator uses the equation: `(Area/Population)*ScaleFactor`
- `Area` refers to the physical size of the city
- `Population` refers total population of the city
- `ScaleFactor` is a constant which scales the result to an easily comprehensible number

### Implementation
Finding Area
- The area of a given city is determined by counting the number of pixels of interest in a 400px by 400px image of the city
- To retrieve this image a call is made to the Mapbox api, giving it the location of the center of the city. TheMapbox API then responds with a 400px by 400px image of the city with a custom map skin designed to enhance the differences between mid-high density residential building and roads, and natural features
- The sprawl-calculator then loops over the retrieved image and counts the number of pixels over a certain brightness threshold as these are likely to be structures which are part of the city (due to the custom Mapbox skin), these are the pixels of interest

Finding Population
- The population of a given city is retrieved from the Geonames API

Finding ScaleFactor
- The scalefactor value of 100 was determined experimentally through testing a few major cities and seeing what range seemed to make the most sense

### Usage
calling the API:
- the flask server portion of this project is currently running on [heroku](https://sprawl-calculator.herokuapp.com/) and takes calls through the form of html get requests
- [heroku/info](https://sprawl-calculator.herokuapp.com/info)
    - call: requires a get request with field city set to the name of the city which you would like info on
    - response: jpeg file of image of city with pixels of interest highlighted (roads and mid-high density housing)
- [heroku/image](https://sprawl-calculator.herokuapp.com/image)
    - call: requires a get request with field city set to the name of the city which you would like an image of
    - response: jpeg file of image of city with pixels of interest highlighted

Examples:
- [heroku/info](https://sprawl-calculator.herokuapp.com/info)
    - call: `https://sprawl-calculator.herokuapp.com/info/?city=boston`
    - response: `{"city_name":"Boston","country":"United States","latitude":"42.35843","longitude":"-71.05977","population":667137,"sprawl_score":5.73}`
- [heroku/image](https://sprawl-calculator.herokuapp.com/image)
    - call: `https://sprawl-calculator.herokuapp.com/image/?city=boston`
    - response: [this image](https://sprawl-calculator.herokuapp.com/image?city=boston)

main.py
- python script which uses sprawl_calculator backend to get sprawl scores and images of inputed cities 
