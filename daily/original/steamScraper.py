#!/usr/bin/python3

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

# hardcoded url from which to scrape
url = "https://store.steampowered.com/search/?specials=1"

# log file used to monitor the scraper
log = open("log", "a")
log.write("Scraping Steam\n")
log.close()

# make the HTTP request and get the HTML data
client = uReq(url)
pageHTML = client.read()
client.close()

# build the BeautifulSoup object from the read html
pageSoup = soup(pageHTML, "html.parser")

# find all of the table rown we are looking for by finding the a tag that they all contain and which contains all necessary data
itemList = pageSoup.findAll("a", {"class":"search_result_row"})

# open the output file in append mode
filename = "results"
f = open(filename, "a")

f.write("STEAM SPECIALS\n\n")

# loop over the items in the list
for item in itemList:

	# find the necessary data:
		# item link
		# item name
		# discount percentage
		# price (normal and discounted)
		# review score
    link = item["href"]

    name = item.findAll("span", {"class":"title"})[0].text

    discount = item.findAll("div", {"class":"search_discount"})[0].span.text

    prices = item.findAll("div", {"class":"search_price"})[0].text.strip().split("$")

    oldPrice = "$" + prices[1]
    newPrice = "$" + prices[2]


    review = item.findAll("span", {"class":"search_review_summary"})[0]["data-tooltip-html"]
    review = review.split(">")[1]
    review = review.split("%")[0] + "%"

	# write data out to the output file
    f.write(name + " | " + review + "\n" + discount + "\n" + oldPrice + " --> " + newPrice + "\n" + link + "\n\n")

f.write("===============================================================================\n\n")

# close the putput file
f.close()
