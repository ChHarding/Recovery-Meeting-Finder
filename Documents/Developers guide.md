# Deployment:
This application does not require installation. The back-end is writen in Python 3+ and requires Beautiful Soup and Pyap packages to run successfully. By running, we mean running `scraper_y12sr.py` and `scraper_smart.py` which eventuates in updating the data of the meetings.
The front-end of this app is writen in HTML/CSS/JavaScript and could be run on any web-server by copying the following files in the same folder:
 * `scraper_y12sr.py`
 * `scraper_smart.py`
 * `geoapify.py`
 * `y12sr.json`
 * `smart.json`
 * `index.html`
 * `style.css`
 * `init_map.js`
 * `functions.js`

# Architecture:
This application is composed of a back-end (Python), and a front-end (HTML/CSS/JavaScript). In the back-end, the data of [Y12SR](https://y12sr.com/) and [SMART Recovery](https://www.smartrecovery.org/) meetings are scraped and stored in JSON format. The following figure shows how the back-end works. `scraper_y12sr.py` and `scraper_smart.py` get the data of the meetings from their websites. In order to prepare the data to be shown on the map, the coordinates are required. So, a third-party API, namely [Geoapify](https://www.geoapify.com/), is utilized to convert the addresses to `{Latitude, Longitude}`. It should be noted that using this API requires an API Key, which is not free. Then, the data are stored in `y12sr.json` and `smart.json`.

The front-end is built in HTML/CSS and vanilla JavaScript, to decrease the complexity and obviate the dependency on other technologies. The data of JSON files are loaded into the app by a JavaScript code. So, as long as all six files (`index.html`, `style.css`, `init_map.js`, `functions.js`, `y12sr.json`, `smart.json` - and of course `img` folder) are in the same directory, the application should work correctly. The UI is accessible by running `index.html`.

<center><img src=https://ronakphotography.com/meetingfinder/architecture.png alt="Architecture of the app: https://ronakphotography.com/meetingfinder/architecture.png"></center> 

# Walkthrough the files:
## Back-end files:
### scraper_y12sr.py
**Goal**: It is a part of the back-end that scrapes the data from https://y12sr.com/meetings/find-a-meeting-by-state/ and stores them as a JSON file.

**Details**: to this goal, we used python requests package for getting the data. The data of the meetings will be received as a text, which the lines are parsed in the `main()` function of the code. The meetings are wrapped in `<div class="wpb_wrapper"></div>` tags. So, we find the chunks of text which contain the meeting data. After cleaning the text from unnecessary tags, such as `<p>`, `<strong>`, `<br />` and `<em>`, the text is parsed to extract the day, time and address (for which we use pyap package) of the meeting. The address is then passed to a function `geoapify()` which returns the coordinates of the location. Finally, the data of meetings is stored in `Y12SR.json` file with the following structure:
```
Ydata = '[
  {
    “days” : [“sundays”],
    “times”: [“15:00”],
    “address”: “an address goes here”,
    “latitude”: “12.3456789”,
    “longitude”: ”98.7654321”,
    “details”: “Other details of the meeting goes here”
  },
  { //next record }
]';
```
Obviously, this is not a standard JSON file. Because, we would like to load it in JavaScript, so we put the JSON content in a string variable, namely `Ydata`.



### scraper_smart
**Goal**: It is a part of the back-end that scrapes the data from https://meetings.smartrecovery.org/meetings/?location=usa&page= and stores them as a JSON file.

**Details**: the data in the source website are presented in several pages. So, this code has two pass to grab the data: in the first pass, it navigates through all the pages to collect the IDs of the meeting pages, and in the second pass, it collects the meeting data from their profile page at: https://meetings.smartrecovery.org/meetings/[meeting Page ID].
Getting the data is done by python requests, and then it is parsed by beautiful soup package. This data includes the day, time, address, latitude, longitude, and other details of the meeting. Finally, the data is stored in a `SMART.json` file, with a structure similar to `Y12SR.json`, except the name of the variable which is `SData`.


### geoapify.py
**Goal**: Two parameters are passed to this class: an address and an API key. Then, it uses a third party service, namely [Geoapify](https://www.geoapify.com/) to get the coordinates of the address. Please note that Geoapify is a paid service. 

**Details**: The code of this class is very straightforward and does not need extra explanation.

## Front-end files:
### index.html
**Goal**: It is the entry point of the UI and is written in HTML.

**Details**: For the background map, we utilize the [Leaflet](https://leafletjs.com/examples/quick-start/). So, the `index.html` starts with adding some JavaScripts and stylesheets that are required for Leaflet. Also, `Y12SR.json` and `SMART.json` are loaded. The last two files that are added are `functions.js` (contains all the functions that we created for working with app) and `style.css` (style of he app). At the end of this file, we load `init_map.js`, which initializes the map and starts the app. All other content of `index.html` are simple HTML code to set up the page.

### init_map.js
**Goal**: It initializes the map.

**Details**: First, a map object is defined and [OpenStreetMap tile](https://www.openstreetmap.org/) is added to it. Then, user's location is obtained and added to the map as a small blue marker. Then, the JSON data of the meetings, which were previously loaded to the app as string variables (in `index.html`) are parsed and the JSON objects are stored in `y12sr` and `smart` variables. At the end, the map is refreshed (`refreshMap()` function is explained in `functions.js` file).


### functions.js
**Goal**: all the required JavaScript functions are defined in this file.

**Details**: Four main functions in this file are:
* `correct_json(jsonString)`: It gets a JSON string and removes all the non-valid JSON characters from it - while parsing the meetings data, since they are scraped from external sources, they might contain non-valid characters.
* `isInRange(timeStr, t1, t2)`: It gets a string containig a time stamp (timeStr), and two other values of type DateTime (t1, t2) that specify a valid time range. Then, it returns True/False if the time string is/isn't in that range.
* `markerClicked(type, days, times, address, details)`: When a "More details ..." button in the marker's popup window is clicked, this functions is run. It opens the left information panel and populates this panel with meeting data.
* `refreshMap()`: This function refreshes the map upon occurence of events, such as changinf the values of the filtering controls (right panel). What it basically does is that it cleas out the all the markers, and reads the values of the filtering control and decides about the data points that must be shown on the map.


### style.css
**Goal**: It contains all the styling settings of the app, used in `index.html`.

**Details**: It is pretty straightforward.

# Known Issues:
So far, no minor or major issues are onserved. 

# Future work:
In continuation of this project, other types of meetings could be added to it. Some examples are: [Alcoholics Anonymous](https://www.aa.org/find-aa), [Narcotics Anonymous](https://www.na.org/meetingsearch/), [Adult Children of Alcoholics](https://adultchildren.org/meeting-search/), and many more.

Also, the UI could be improved to become more accessible, and usable.


