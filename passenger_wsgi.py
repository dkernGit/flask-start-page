from personal_start import StartPage

from flask import Flask, render_template, request
application = Flask('__name__')


@application.route('/')
def index():
    # Check GET request arguments for user's name, city and state argument for greeting and weather api
    user = request.args.get('user')
    state = request.args.get('state')
    city = request.args.get('city')
    

    if user and city:
        if state:
            content = StartPage(user,city,state)
        else:
            content = StartPage(user,city)
    elif user:
        content = StartPage(user)
    else:
        content = StartPage()

    if request.args.get('cam') == "OR":
        content.cam = 'OR'

    webcam1, webcam2 = content.webcams()

    if request.args.get('tides') == "Y":
        tide_table = content.tides()
    else:
        tide_table = []

    background = content.my_bg()

    data = {
        "greeting": content.greeting,
        "greet_name": content.user,
        "weather": content.weather_data,
        "sunset": (str(content.sunrise), str(content.sunset)),
        "zip": content.zip,
        "cam1": webcam1,
        "cam2": webcam2,
        "tides": tide_table,
        "tides_station": content.station_id,
        "background": background[0],
        "background_u": background[1],
        "background_c": background[2],
    }
    return render_template('startpage.html', data=data)