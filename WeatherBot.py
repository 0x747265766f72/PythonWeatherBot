import requests, json, geocoder, astral, geopy, suntime, time, math, re, smtplib, pytz, datetime
from time import time, sleep, mktime
from timezonefinder import TimezoneFinder
from astral.sun import sun
from astral import moon
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# APIs, Credentials, and Global email Variables
# https://openweathermap.org/current
credFile = open('creds.json')
credJson = json.load(credFile)

openWeather_API_Key = credJson['openWeather_API_Key']
accuWeather_API_Key = credJson['accuWeather_API_Key']

# https://towardsdatascience.com/automate-email-sending-with-python-74128c7ca89a 
bot_email = 'weatherbotsupreme@gmail.com'
bot_password = credJson['bot_password']
toList = credJson['toList']
HOST_ADDRESS = 'smtp.gmail.com'
HOST_PORT = 587

# Open json file containing schedule of meteor showers
# Source: https://www.almanac.com/content/meteor-shower-calendar 
MeteorFile = open('MeteorShowerCalendar.json')
MeteorJson = json.load(MeteorFile)

# Primary Method to Update Current Location Data
def location_update():
    # https://geocoder.readthedocs.io/
    g = geocoder.ip('me')
    lati = g.latlng[0]
    lngi = g.latlng[1]
    city = g.city
    state = g.state
    # https://geopy.readthedocs.io/en/stable/
    # https://www.geeksforgeeks.org/get-the-city-state-and-country-names-from-latitude-and-longitude-using-python/ 
    cunt = geopy.geocoders.Nominatim(user_agent="geoapiExercises")
    location = cunt.reverse(str(lati)+","+str(lngi))
    address = location.raw['address']
    country = address.get('country_code')
    country = country.upper()
    obj = TimezoneFinder()
    tz_info = obj.timezone_at(lat = lati, lng = lngi)
    return_info = [lati, lngi, city, state, country, tz_info]
    return return_info

# Primary Method to Update current time data
def now_time():
    currentTime = mktime(datetime.datetime.utcnow().timetuple())
    now = datetime.datetime.now()
    timeObj = [now, currentTime]
    return(timeObj)

# Primary Dusk Time Method [Supplement data for AuroraMain()]
def dusk_time():
    loc_update = location_update()
    lati = loc_update[0]
    lngi = loc_update[1]
    city = loc_update[2]
    state = loc_update[3]
    country = loc_update[4]
    tz_info = loc_update[5]

    Y = now_time()[0].year
    M = now_time()[0].month
    D = now_time()[0].day

    region_info = state+", "+country
    loc = astral.LocationInfo(name=city, region=region_info, timezone=tz_info, latitude=lati, longitude=lngi)
    s = astral.sun.sun(loc.observer, date=datetime.date(Y, M, D))
    duskTime = s["dusk"]
    duskTime = mktime(duskTime.timetuple())
    return(duskTime)

# Primary Moon Phase Method [Supplement data for AuroraMain()]
def MoonPhase():
    moonphase = astral.moon.phase(now_time()[0])
    if moonphase < 7:
        status = "New Moon"
    elif 7 <= moonphase < 14:
        status = "First Quarter"
    elif 14 <= moonphase < 21:
        status = "Full moon"
    elif 21 <= moonphase < 28:
        status = "Last Quarter"
    return status

def MeteorMsg():
    Y = now_time()[0].year
    M = now_time()[0].month
    D = now_time()[0].day
    datestring = str(M)+"/"+str(D)+"/"+str(Y)
    
    # datestring = "8/12/2022"
    weather = weatherRun()
    cloudcover = weather[2]
    outmsg = ""
    for i in range(12):
        for j in range(3):
            date = "DATE"
            if j == 1:
                date = "DATE__1"
            if j == 2:
                date = "DATE__2"
            if datestring == MeteorJson[i][date]:
                shower = MeteorJson[i]["SHOWER"]
                bestView = MeteorJson[i]["BEST VIEWING"]
                origin = MeteorJson[i]["POINT OF ORIGIN"]
                metPerHr = MeteorJson[i]["NO. PER HOUR**"]
                bigBoy = MeteorJson[i]["ASSOCIATED COMET"]
                outmsg = "Meteor Shower Tonight\n\tShower:\t\t\t"+shower+"\n\tMeteors Per Hour:\t"+str(metPerHr)+"\n\tCommet to Watch for:\t"+bigBoy+"\n\tBest Time To View:\t"+bestView+"\n\tDirection of Shower:\t"+origin+"\n\tCloud Cover:\t"+str(cloudcover)+"%"
    if outmsg is not None:
        return(outmsg)
    else:
        return

# Primary Weather Method
def Weather():
    loc_update = location_update()
    lati = loc_update[0]
    lngi = loc_update[1]
    weatherURL = "https://api.openweathermap.org/data/2.5/weather?lat="+str(lati)+"&lon="+str(lngi)+"&appid="+openWeather_API_Key
    weather_response = requests.get(weatherURL)
    return(weather_response)

# Termerature Unit Conversion
def KeltoF(keltemp):
    keltemp = int(keltemp)
    cel = keltemp - 273.15
    far = cel*(9/5)+32
    return math.floor(far)

# Weather Data Format Method
def weatherRun():
    outside = Weather().json()
    temp = KeltoF(outside["main"]["temp"])
    WC = KeltoF(outside["main"]["feels_like"])
    low = KeltoF(outside["main"]["temp_min"])
    high = KeltoF(outside["main"]["temp_max"])
    wind = outside["wind"]["speed"]
    conditions = outside["weather"][0]["description"]
    cloudcover = outside["clouds"]["all"]
    city = outside["name"]
    state = location_update()[3]
    dayName = now_time()[0].strftime("%A")
    monthName = now_time()[0].strftime("%B")
    dateNum = now_time()[0].strftime("%d")
    dateNum = int(dateNum)
    if 4 <= dateNum <= 20 or 24 <= dateNum <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][dateNum % 10 - 1]
    date = str(dateNum)+suffix

    weatherReport = "\n_-_-_-_-_-_-_-Good Morning Trevor_-_-_-_-_-_-_-\n\nToday is "+dayName+", " + monthName +" "+ date +"\n\nHere is the current weather report for "+str(city)+", "+state+"\n\n\tCurrently it is: "+str(temp)+" degrees out\n\tThe windchill is: " + str(WC) + " degrees\n\tThe high for today is "+ str(high) + " degrees\n\tThe low is "+ str(low)+ " degrees\n\tCurrent Weather Contition Report: "+conditions + "\n\tCurrent cloud cover is: "+str(cloudcover)+"%"
    return [weatherReport, conditions, cloudcover, temp, WC, wind]
    # index [0] for good morning message

# Primart Aurora Method
def AuroraRun():
    weaterdata = weatherRun()
    cond = weaterdata[1]
    cloud = weaterdata[2]
    temp = weaterdata[3]
    windms = weaterdata[5]
    windmph = int(windms)*2.237
    wc = weaterdata[4]
    moonphase = MoonPhase()
    moon = moonphase

    # https://www.swpc.noaa.gov/communities/space-weather-enthusiasts
    auroraURL = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"
    r = requests.get(auroraURL)
    src = r.text
    kpmsg = re.search(r'The greatest expected 3 hr Kp for.*\d\d\d\d is (\d) .* NOAA', src)
    NOAAkpindex = kpmsg.group(1)
    NOAAkpindex = int(NOAAkpindex)
    # NOAAkpindex = 5
    outmsg = ""
    if NOAAkpindex == 3 or cloud >= 75:
        outmsg = "LOW possibility of seeing the lights tonight\n\tGreatest expected KP (3hr): " + str(NOAAkpindex) +"\n\tCurrent Cloud Coverage: " + str(cloud) +"%\n\tCurrent Weather Conditions: "+str(cond)+"\n\tMoon Phase: "+str(moon)+"\n\tCurrent Temp: "+str(temp)+" degrees"+"\n\tWindchill: "+str(wc)+" degrees"+"\n\tCurrent wind speeds: "+str(windmph)+" MPH"
    elif 3 < NOAAkpindex <= 4 or cloud >= 33:
        outmsg = "Possibility of seeing the lights tonight\n\tGreatest expected KP (3hr): " + str(NOAAkpindex) +"\n\tCurrent Cloud Coverage: " + str(cloud) +"%\n\tCurrent Weather Conditions: "+str(cond)+"\n\tMoon Phase: "+str(moon)+"\n\tCurrent Temp: "+str(temp)+" degrees"+"\n\tWindchill: "+str(wc)+" degrees"+"\n\tCurrent wind speeds: "+str(windmph)+" MPH"
    elif NOAAkpindex > 4 and cloud < 33:
        outmsg = "HIGH Possibility of seeing the lights tonight\n\tGreatest expected KP (3hr): " + str(NOAAkpindex) +"\n\tCurrent Cloud Coverage: " + str(cloud) +"%\n\tCurrent Weather Conditions: "+str(cond)+"\n\tMoon Phase: "+str(moon)+"\n\tCurrent Temp: "+str(temp)+" degrees"+"\n\tWindchill: "+str(wc)+" degrees"+"\n\tCurrent wind speeds: "+str(windmph)+" MPH"
    return [outmsg, cloud, moon, NOAAkpindex]

# Snow Check Method
def snowCheck():
    loc_update = location_update()
    lati = loc_update[0]
    lngi = loc_update[1]

    accuLocURL = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey="+str(accuWeather_API_Key)+"&q="+str(lati)+"%2C"+str(lngi)
    outmsg = ""
    try:
        accuLocRes = requests.get(accuLocURL)
        accuLocResJson = accuLocRes.json()
        loc_key = accuLocResJson["Key"]

        accu12hrURL = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/"+str(loc_key)+"?apikey="+str(accuWeather_API_Key)

        accu12hRes = requests.get(accu12hrURL)
        forecast12h = accu12hRes.json()
        
        i = 0
        while i < 12:
            precipProb = forecast12h[i]['PrecipitationProbability']
            hasPrecip = forecast12h[i]['HasPrecipitation']
            if hasPrecip == True:
                precipType = forecast12h[i]['PrecipitationType']
                if precipType == "Snow":
                    precipIntensity = forecast12h[i]['PrecipitationIntensity']
                    tz = location_update()
                    timezone = tz[5]
                    local_time = datetime.datetime.now(pytz.timezone(str(timezone)))
                    
                    rainTime = int(i)+int(local_time.hour)

                    outmsg = outmsg + "\tAt "+str(rainTime)+":00, there is a "+str(precipProb) +"% Chance of "+str(precipIntensity)+" "+str(precipType)+"\n"
            i+=1
    except:
        pass
    if len(outmsg) != 0:
        return outmsg
    else:
        return

# Format Aurora Data
def AuroraMain():
    AuroraCall = AuroraRun()
    shaft = AuroraCall[0]
    cloud = AuroraCall[1]
    kp = AuroraCall[3]
    moon = AuroraCall[2]
    
    if cloud < 25:
        if int(now_time()) >= int(dusk_time()) and moon == "Full moon" or "New Moon":
            sendMail("Slim chance for lights", "You probably won't see the lights tonight, but it should be a good night for skywatching!\n\n\tCurrent Cloud Coverage is: " + str(cloud)+"%\n\tCurrently moon phase: "+moon+"\n\tCurrent KP: "+kp)
        else:
            return
    else:
        return

# Mail method
def sendMail(subject, messagetext, mailList):
    for address in mailList:
        message = MIMEMultipart()
        message['From'] = bot_email
        message['To'] = address
        message['Subject'] = subject
        textPart = MIMEText(messagetext)
        message.attach(textPart)
        server = smtplib.SMTP(host=HOST_ADDRESS, port=HOST_PORT)
        server.starttls()
        server.login(bot_email, bot_password)
        server.send_message(message)
        server.quit()

# Secondary Calls for Daily Forecast, Aurora Forecast, and 12 Snow Forecast
def GoodMorningVietnam():
    morningCall = weatherRun()
    morningMsg = morningCall[0]
    sendList = [toList[0]]
    sendMail("Good Morning", morningMsg, sendList)
    return

def NorthernFuckingLights():
    AuroraCall = AuroraRun()
    AuroraMsg = AuroraCall[0]
    
    sendList = [toList[0], toList[1], toList[2]]

    if len(AuroraMsg) != 0:
        sendMail("Northern Lights Forecast", AuroraMsg, sendList)
        return
    else:
        return

def WhiteShitFallingFromTheSky():
    snowMsg = snowCheck()
    if str(type(snowMsg)) != "<class 'NoneType'>":
        sendList = [toList[0]]
        sendMail("Snow Forecast", snowMsg, sendList)
        return
    else:
        return

def SkyRocks():
    MetCall = MeteorMsg()
    if len(MetCall) != 0:
        sendList = [toList[0], toList[1], toList[2]]
        sendMail("Meteor Shower Alert", MetCall, sendList)
        return
    else:
        return

# # Looping to check times and run secondart calls
while True:
    hour = now_time()[0].strftime("%H")
    min = now_time()[0].strftime("%M")
    if min == "00":
        # 9:00 AM
        if hour == "09":
            GoodMorningVietnam()
            WhiteShitFallingFromTheSky()
        # 9:00 PM
        elif hour == "21":
            NorthernFuckingLights()
            WhiteShitFallingFromTheSky()
            SkyRocks()
        # 00:00 (midnight)
        elif hour == "00":
            NorthernFuckingLights()
        
    # Sleep for 1 minute before checking the time again
    sleep(60 - time() % 60)



# # Calls for Testing

# GoodMorningVietnam()
# NorthernFuckingLights()
# WhiteShitFallingFromTheSky()
# SkyRocks()