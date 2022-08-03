'''
====================================================================
It is a part of the back-end that scrapes the ID of meeting pages from
https://meetings.smartrecovery.org/meetings/?location=usa&page=
and the contents of the meeting pages by their IDs from
https://meetings.smartrecovery.org/meetings/[ID]
and stores them as a JSON file.

Input: None
Output: SMART.json

Dependents: Front-end requires the Y12SR.json to show the meetings
             on the map.
Dependency: BeautifulSoup package
====================================================================
'''

import requests
import json
from bs4 import BeautifulSoup, Comment


import warnings
warnings.filterwarnings('ignore')


apiKey = "XXXXXXX" # Key is removed because it is a public repository





def main():

    url = "https://meetings.smartrecovery.org/meetings/?location=usa&page="

    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}




    # ===== scrape all the pages to extract meeting IDs ======================

    pageNum = 1
    page = requests.get(url + str(pageNum), headers=header).text

    pageIDs = []

    while "<title>Not Found</title>" not in page and "<h1>Not Found</h1><p>The requested resource was not found on this server.</p>" not in page:
        print("Getting meeting IDs from page " + str(pageNum), end="\r")

        lines = page.split("\n")

        for line in lines:
            if "data-href=\"/meetings/" in line:
                pageID = line.replace("data-href=\"/meetings/","").replace("/\"","")
                if pageID.isnumeric():
                    pageIDs.append(int(pageID))

        pageNum += 1
        page = requests.get(url + str(pageNum), headers=header).text

    pageIDs.sort()
    print(pageIDs)
    print(str(len(pageIDs)) + " Smart recovery meetings are found!")




    # ===== Get meeting info from meeting pages ======================
    meetingPage = "https://meetings.smartrecovery.org/meetings/"


    jsonData = []

    for pageID in pageIDs:

        page = requests.get(meetingPage + str(pageID), headers=header)

        soup = BeautifulSoup(page.content, 'html.parser')

        cards = soup.find_all('div', class_='card')

        details = ""


        for card in cards:
            cardHeader = card.find('div', class_='card-header').get_text().replace("\n", "").strip()
            onlineLink = ""

            if (cardHeader == "Start Time"):
                dayTimeString = card.find('p', class_='card-text').get_text().replace("\n", "").strip()
                dayTimeWords = dayTimeString.split(" ")
                days = dayTimeWords[0].lower()
                times = dayTimeWords[1].lower() + " " + dayTimeWords[2].lower()

            elif (cardHeader == "Location"):
                cardBody = card.find('div', class_='card-body').get_text().replace("\n", "").strip()
                cardText = card.find('p', class_='card-text').get_text().replace("\n", "").strip()
                if "Get Directions" in cardBody:
                    meetingType = "in-person"
                    #print(cardText)
                    address = cardText.replace("                ", ", ")

                    while ", , " in address:
                        address = address.replace(", , ", ", ")

                    while "  " in address:
                        address = address.replace("  "," ")
                    #print(address)

                else:
                    meetingType = "online"
                    address = cardText.replace("This online meeting is run out of ", "")
                    address = address.replace(". Curious about what's nearby? Take a look!", "")

                comment = " ".join(soup.find_all(text=lambda text:isinstance(text, Comment)))
                idxLatLng = comment.find("myLatLng = { lat: ")
                latLngString = comment[idxLatLng+12 : ]
                latLngString = latLngString.split("}")[0].strip()
                #print(latLngString)
                latLng = [coord.strip() for coord in latLngString.split(",")]

                if "lat" in latLng[0]:
                    lat = latLng[0].split(" ")[1]
                    lng = latLng[1].split(" ")[1]
                elif "lat" in latLng[1]:
                    lat = latLng[1].split(" ")[1]
                    lng = latLng[0].split(" ")[1]


            elif (cardHeader == "Online Meeting"):
                onlineLink = card.find_all('a', href=True)
                if onlineLink:
                    onlineLink = onlineLink[-1]['href']

            else:
                detail = card.get_text().strip() + "\n"

                detail = detail.replace("                ", "\n")

                while "\n\n" in detail:
                    detail = detail.replace("\n\n", "\n")

                while "  " in detail:
                    detail = detail.replace("  "," ")

                detail = detail.replace("\n ", "\n")

                details += detail + "\n\n\n"


        #print(days, times, meetingType, address, lat, lng, onlineLink, details)
        #print(len(cards))

        newRecString = "{\"days\": ['" + days + "'], \"times\": ['" + times + "'], \"address\": \"" + address.replace("\"", "").replace("\'","") +  "\"" + ", \"latitude\": \"" + str(lat) + "\"" + ", \"longitude\": \"" + str(lng) + "\"" +  " , \"details\": \"" + details.replace("\"", "").replace("\'","") + "\"}"
        newRecString = newRecString.replace("\'", "\"")
        print(newRecString)
        newRec = json.loads(newRecString, strict=False)
        jsonData.append(newRec)

    f = open('SMART.json', 'w')
    f.write("SData = '" + json.dumps(jsonData) + "';")



main()
