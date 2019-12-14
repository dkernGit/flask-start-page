import requests
import os
from datetime import datetime
from datetime import timedelta
from pytz import timezone
from random import choice


class StartPage():
    def __init__(self, user="Friend", city="Coos Bay", state="OR", cam="CA"):
        self.user = user
        self.city = city
        self.state = state
        self.cam = cam
        pac_tz = timezone("US/Pacific")
        self.daytime = datetime.now(pac_tz)
        self.greeting = "Day"
        self.user_greeting()
        self.lat='43.36999893'
        self.lng='-124.22000122'
        self.zip='97420'
        self.station_id = '9432780'
        self.weather_data = {}
        # self.weather_ext = {}
        self._weather()
        self.sunrise = self.daytime
        self.sunset = self.daytime
        self._sunrise_sunset()


    def my_bg(self):
        url = "/bgs/"
        credit = ""
        return (url + choice(os.listdir("public/static/bgs/")),"kernimg", credit)


    def _weather(self):
        with open('geokey.txt') as f:
            geokey = f.readline()
        
        map_url ="http://open.mapquestapi.com/geocoding/v1/address?key=" + geokey + "&location="
        map_url = map_url + self.city + "," + self.state

        map_json = requests.get(map_url).json()
        self.lat = str(map_json['results'][0]['locations'][0]['latLng']['lat'])
        self.lng = str(map_json['results'][0]['locations'][0]['latLng']['lng'])

        points_url = "https://api.weather.gov/points/" + self.lat + "," + self.lng
        points_json = requests.get(points_url).json()

        weather_url = points_json['properties']['forecastHourly']
        weather_json = requests.get(weather_url).json()

        weather_temp = str(weather_json['properties']['periods'][0]['temperature'])

        weather_temp = weather_temp + " " + weather_json['properties']['periods'][0]['temperatureUnit']

        points_city = points_json['properties']['relativeLocation']['properties']['city']
        points_state = points_json['properties']['relativeLocation']['properties']['state']
        weather_forecast = weather_json['properties']['periods'][0]['shortForecast']
        weather_icon = weather_json['properties']['periods'][0]['icon']

        station_url = "https://forecast.weather.gov/MapClick.php?lat=" + self.lat +"&lon=" + self.lng
        weather_observe = {"city": points_city + ", " + points_state,
                           "curr_temp": weather_temp,
                           "forecast": weather_forecast,
                           "icon_url": weather_icon,
                           "station_url": station_url,
                           "lat": self.lat,
                           "lng": self.lng  }

        self.weather_data = weather_observe
        self.zip = '97420'


    def user_greeting(self):
        if self.daytime.hour < 12:
            self.greeting = "Morning"
        elif self.daytime.hour >= 12 and self.daytime.hour < 17:
            self.greeting = "Afternoon"
        else:  # daytime.hour >= 17 and daytime.hour <= 23
            self.greeting = "Evening"


    def _sunrise_sunset(self):
        # Sunrise/Sunset API for Lat an Lng coordinates
        time_url = "https://api.sunrise-sunset.org/json?lat=" + self.lat +\
                   "&lng=" + self.lng + "&formatted=0" + "&date=" +\
                   datetime.strftime(self.daytime,"%Y-%m-%d")
        sunset_res = requests.get(time_url).json()
        self.sunset = datetime.strptime(sunset_res["results"]['sunset'][:18],
                     "%Y-%m-%dT%H:%M:%S") # - timedelta(hours=7)
        la = timezone('America/Los_Angeles')
        self.sunset = la.fromutc(self.sunset)
        self.sunrise = datetime.strptime(sunset_res["results"]['sunrise'][:18],
                      "%Y-%m-%dT%H:%M:%S") # - timedelta(hours=7)
        self.sunrise = la.fromutc(self.sunrise)


    def tides(self):
        # NOAA Tides Data for station ID - i.e. 9432780
        station_dict = requests.get("https://tidesandcurrents.noaa.gov/mdapi/v1.0/webapi/stations.json").json()
        state_stations = [li for li in station_dict['stations'] if li['state'] == self.state]
        lats = [li['lat'] for li in state_stations]
        city_lat = float(self.lat)
        lat_loc = min(range(len(lats)), key=lambda x:abs(lats[x]-city_lat))
        self.station_id = state_stations[lat_loc]['id']
        
        t_url = "https://tidesandcurrents.noaa.gov/api/datagetter?" +\
                "product=predictions&application=NOS.COOPS.TAC.WL&begin_date="+\
                datetime.strftime(self.daytime,"%Y%m%d") + "&range=24" +\
                "&datum=MLLW&station=" + self.station_id +\
                "&time_zone=lst_ldt&units=english" +\
                "&interval=hilo&format=json"
        tide_res = requests.get(t_url).json()
        #tide_table = [t['t'] + ' ' + t['v'] for t in tide_res["predictions"]]
        tide_table = []
        for t in tide_res['predictions']:
            if t['type'] == 'H':
                tide_table.append('High Tide: ' + t['t'] + ' ' + t['v'])
            else:
                tide_table.append('Low Tide: ' + t['t'] + ' ' + t['v'])
        return tide_table


    def webcams(self):
        if self.cam=="CA":
            if (self.daytime.hour <= self.sunset.hour and
                self.daytime.hour >= self.sunrise.hour):
                webcam = {'url': "https://portal.hdontap.com/snapshot/kingsbeach_ttv-TOPIA?" +\
                               "overlay=yes&position=ll&size=640x360&overlay_image=upload_" +\
                               "79915e70da64d0c2232752be3729d9e5.png&padx=10&pady=10",
                          'source': "http://tahoetopia.com/webcam/kings-beach-north-tahoe-watersports-cam",
                          'credit': "Kings Beach Live Webcam"
                }
                webcam2 = {'url': "https://pixelcaster.com/yosemite/webcams/sentinel.jpg",
                           'source': "https://www.yosemiteconservancy.org/webcams/high-sierra",
                           'credit': "Yosemite High Sierra Webcam"
                }
            else:
                webcam = {'url': "https://shop.keeptahoeblue.org/data/products/" +\
                               "images/7/6/5/large.jpg",
                          'source': "https://shop.keeptahoeblue.org/data/products/",
                          'credit': "Keep Tahoe Blue"
                }
                webcam2= ""
        else:
            if (self.daytime.hour <= self.sunset.hour and
                self.daytime.hour >= self.sunrise.hour):
                webcam = {'url': "https://oregonstateparks.org/view/conditions/shoreacres000M.jpg?1522809549688",
                          'source': "https://oregonstateparks.org/index.cfm?do=conditions.dsp_parkConditions&parkId=70",
                          'credit': "Sunset Bay State Park"
                }
                webcam2 = {'url': "https://www.nps.gov/webcams-crla/camerasinnott.jpg",
                           'source': "https://www.nps.gov/customcf/webcam/dsp_webcam_image.cfm?id=81B4629B-1DD8-B71B-0BAE9CC7158D1E56",
                           'credit': "Crater Lake Sinnott Memorial Overlook Webcam"
                }
            else:
                webcam = {'url': "http://www.xanterra.net/cratercam/cam_2.jpg",
                          'source': "http://www.craterlakelodges.com/webcam/",
                          'credit': "Crater Lake Lodge Webcam"
                }
                webcam2= ""
        return (webcam, webcam2)
