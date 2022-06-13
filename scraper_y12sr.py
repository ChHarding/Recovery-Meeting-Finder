
import requests
#import json
#from six.moves import configparser


import warnings
warnings.filterwarnings('ignore')

''' --> Will be used later to read the database configuration from ini file

config = configparser.ConfigParser()
config.read('./config/config.ini')
username = config.get('CREDENTIALS','username')
password = config.get('CREDENTIALS','password')
host     = config.get('CREDENTIALS','host')
database = config.get('CREDENTIALS','database')
backups  = config.get('CREDENTIALS','backups')
'''



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
                        meeting = meeting.replace("\n ","\n")
                        meeting = meeting.strip()
                        if meeting != "":
                            allMeetings.append(meeting)
                    wrappers.append(chunk)


f = open('Y12SR.txt', 'w')

for meeting in allMeetings:
    f.write(meeting + "\n\n")
