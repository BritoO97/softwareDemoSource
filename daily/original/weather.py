#!/usr/bin/python3

from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen


# hardcoded url from which to scrape
url ="https://weather.com/weather/tenday/l/USNJ0355:1:US"

# log file used to monitor the scraper
log = open("log", "a")
log.write("Getting Weather Forecast\n")
log.close()

# file to which all results are written to
filename = "results"

# make the HTTP request to the page using a custom header
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

# send the request and read the page contents
pageHTML = urlopen(req).read()

# build the BeautifulSoup object from the read html
pageSoup = soup(pageHTML, "html.parser")

# find the table containing the daily forecasts and pick the first table row
# the first table row will contain the forecast for the day in which the script is ran
row = pageSoup.findAll("tr", {"class":"clickable closed"})[0]

# retrieve all of the td tags that contain the data needed
content = row.findAll("td")

# retrieve the wanted data from the various td tags
# description will be the 3rd tag
# high and low temperature will be on the 4th tag
# rain/snow chance will be the 5th tag
# humidity will be the 7th tag
desc = content[2].span.text

tempLow = content[3].div.findAll("span")[0].text
tempHigh = content[3].div.findAll("span")[2].text

prec = content[4].div.findAll("span")[1].span.text

hum = content[6].span.span.text

# open the results file in append mode
f = open(filename, "a")

# write the data out to a file with some formating
f.write("WEATHER FORECAST\n\n")

f.write("Description: " + desc + "\nTemp: " + tempLow + " / " + tempHigh + "\nRain/Snow: " + prec + "\nHumidity: " + hum + "\n\n===================================================================================\n\n")

# close the file when donw
f.close()
