
import requests
import json
import pyap
from geoapify import geoapify
#from six.moves import configparser


import warnings
warnings.filterwarnings('ignore')


apiKey = "XXXXXXX" # Key is removed because it is a public repository


''' --> Will be used later to read the database configuration from ini file

config = configparser.ConfigParser()
config.read('./config/config.ini')
username = config.get('CREDENTIALS','username')
password = config.get('CREDENTIALS','password')
host     = config.get('CREDENTIALS','host')
database = config.get('CREDENTIALS','database')
backups  = config.get('CREDENTIALS','backups')
'''








def main():

    url = "https://y12sr.com/meetings/find-a-meeting-by-state/"


    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}

    page = requests.get(url, headers=header).text

    lines = page.split("\n")

    wrappers = []
    allMeetings = []

    i = 0
    while (i<len(lines)):
        line = lines[i].strip()
        i += 1
        if(line == '<div class="wpb_wrapper">' or line == "<div class='wpb_wrapper'>" or line == "<div class=wpb_wrapper>"):
            chunk = ""
            line = lines[i].strip()
            while (line != "</div>"):
                chunk = chunk + line + "\n"
                i += 1
                line = lines[i].strip()


            if(chunk):
                if(len(chunk)>11):
                    if(chunk[:11] == "<p><strong>"):
                        chunk = chunk.replace("</strong></p>\n<p><strong>", "\n")
                        meetings = chunk.split("<p><strong>")
                        for meeting in meetings:
                            meeting = meeting.replace("<br />"," ").replace("<div>"," ").replace("</div>"," ").replace('<div dir="ltr">'," ")
                            meeting = meeting.replace("<em>"," ").replace("</em>"," ").replace("<strong>"," ").replace("</strong>"," ").replace("<p>"," ").replace("</p>"," ")
                            meeting = meeting.replace("\n ","\n")
                            meeting = meeting.strip()
                            if meeting != "":
                                allMeetings.append(meeting)
                        wrappers.append(chunk)


    jsonData = []

    f = open('Y12SR.json', 'w')

    for meeting in allMeetings:

        days,times = day_time(meeting)
        if (days and times):

            daysStr = ""
            for day in days:
                daysStr += "'" + day + "',"
            daysStr = "[" + daysStr[:-1] + "]"

            timesStr = ""
            for time in times:
                timesStr += "'" + time+"',"
            timesStr = "[" + timesStr[:-1] + "]"
            address = str(parse_address(meeting.replace("\n", "")))

            lat = "-"
            lon = "-"

            if address != "-":
                try:
                    name, city, county, state, country, country_code, formatted, lon, lat, result_type, confidence, confidence_city_level, match_type = geoapify(address, apiKey)
                except:
                    lat = "-"
                    lon = "-"

            if lat == "":
                lat = "-"
            if lon == "":
                lon = "-"

            newRecString = "{\"days\":" + daysStr + ", \"times\": " + timesStr + ", \"address\": \"" + address +  "\"" + ", \"latitude\": \"" + str(lat) + "\"" + ", \"longitude\": \"" + str(lon) + "\"" +  " , \"details\": \"" + meeting.replace("\"", "") + "\"}"
            newRecString = newRecString.replace("\'", "\"")
            print(newRecString)
            newRec = json.loads(newRecString, strict=False)
            jsonData.append(newRec)

    f.write("YData = '" + json.dumps(jsonData) + "';")







def day_time(meetingString): #extract day name and time from the string
    meetingDays = []
    meetingTimes = []

    days = ["mondays", "tuesdays", "wednesdays", "thursdays", "fridays", " saturdays", "sundays"]
    for day in days:
        for line in meetingString.split("\n"):
            if day in line.lower():
                line = line.lower()
                line = line.replace(day,"")
                line = line.replace(" | ","")
                line = line.replace(" at ","")
                line = line.replace("(pst)","").replace("(gmt)","").replace("(cst)","").replace("(est)","").replace("(cdt)","").replace("(aedt)","").replace("(pdt)","").replace("(mst)","")
                line = line.strip()
                splitLine = line.split(":")
                if len(splitLine)<2:
                    continue
                hour = splitLine[0].split(" ")[-1]
                splitLine[1] = splitLine[1].replace("am", " am").replace("pm", " pm").replace("   ", " ").replace("  "," ")
                minutes = splitLine[1].split(" ")[0]
                try:
                    ampm = splitLine[1].split(" ")[1]
                except:
                    ampm = ""

                #test if time is correct:
                if (hour.isnumeric() and minutes.isnumeric()):
                    if ampm == "am" or ampm=="pm":
                        timeString = hour + ":" + minutes + " " + ampm
                    else:
                        timeString = hour + ":" + minutes
                else:
                    continue

                meetingDays.append(day)
                meetingTimes.append(timeString)

    return meetingDays,meetingTimes




def parse_address(addr):
    address = pyap.parse(addr, country = "US")
    if not address:
        address = pyap.parse(addr, country = "CA")
    if not address:
        address = pyap.parse(addr, country = "GB")
    if address:
        return address[0]
    else:
        return "-"



main()
