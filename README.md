# Recovery Meeting Finder


## Introduction
Finding the recovery meetings in your desired time and location is usually challenging, because it requires navigating through several websites of different types of recovery meetings to find a proper one. Two types of recovery meetings that remaind rather unknown are [Y12SR](https://y12sr.com/) and [SMART recovery](https://www.smartrecovery.org/) meetings. This tool, aims at providing easy access to the information of these meetings to the end users.



## Demo
Here is a [live demo](https://ronakphotography.com/meetingfinder/) of this project.

![Preview available at: https://ronakphotography.com/meetingfinder/preview.gif](https://ronakphotography.com/meetingfinder/preview.gif)



## How does it work?
This application is composed of a back-end (Python), and a front-end (HTML/CSS/JavaScript). In the back-end, the data of [Y12SR](https://y12sr.com/) and [SMART Recovery](https://www.smartrecovery.org/) meetings are scraped and stored in JSON format. The following figure shows how the back-end works. `scraper_y12sr.py` and `scraper_smart.py` get the data of the meetings from their websites. In order to prepare the data to be shown on the map, the coordinates are required. So, a third-party API, namely [Geoapify](https://www.geoapify.com/), is utilized to convert the addresses to `{Latitude, Longitude}`. It should be noted that using this API requires an API Key, which is not free. Then, the data are stored in `y12sr.json` and `smart.json`.

The front-end is built in HTML/CSS and vanilla JavaScript, to decrease the complexity and obviate the dependency on other technologies. The data of JSON files are loaded into the app by a JavaScript code. So, as long as all six files (`index.html`, `style.css`, `init_map.js`, `functions.js`, `y12sr.json`, `smart.json` - and of course `img` folder) are in the same directory, the application should work correctly. The UI is accessible by running `index.html`.

<center><img src=https://ronakphotography.com/meetingfinder/architecture.png alt="Architecture of the app: https://ronakphotography.com/meetingfinder/architecture.png"></center>



## How to set up the application on a new server (VPS)?

1. Get an API key from [Geoapify](https://www.geoapify.com/). Edit the `scraper_y12sr.py` and `scraper_smart.py` and add your key.
2. Copy all the following files to a directory in your website path (all in the same folder):
 * `scraper_y12sr.py`
 * `scraper_smart.py`
 * `y12sr.json`
 * `smart.json`
 * `index.html`
 * `style.css`
 * `init_map.js`
 * `functions.js`
3. Schedule the `scraper_xxxxx.py` files to run every day/week/month, according to your needs. Running these files will update the data of the meetings. For running them you will need Python 3+. Execute this command: `python scraper_xxxxx.py`
4. Use the app by going to its path on your website.


