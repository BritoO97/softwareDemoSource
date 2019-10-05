#!/usr/bin/python3

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import json

# hardcoded url from which to scrape
url = "https://www.gog.com/games/ajax/filtered?mediaType=game&page=1&price=discounted&sort=popularity"

# log file used to monitor the scraper
log = open("log", "a")
log.write("Scraping GOG\n")
log.close()

# make the HTTP request and read the JSON data
client = uReq(url)
pageJSON = json.loads(client.read().decode("utf-8"))
client.close()

# open the output file in append mode
filename = "results"
f = open(filename, "a")

f.write("GOG SPECIALS\n\n")

# find the item list
products = pageJSON["products"]

# iterate over the top 25 results from the item list
for i in range(0,25): 
	# select the item at the current index
    item = products[i]
    
	# find the necessary data:
		# item link
		# item name
		# discount percentage
		# price (normal and discounted)
		# review score
    priceObj = item["price"]
    discount = priceObj["discount"]
    regPrice = priceObj["baseAmount"]
    newPrice = priceObj["amount"]

    name = item["title"]
    score = item["rating"] * 2

    link = "www.gog.com" + item["url"]

	# write data to the output file
    f.write(name + " | " + str(score) + "%\n")
    f.write("-" + str(discount) + "%\n")
    f.write("$" + str(regPrice)+ " --> $" + str(newPrice) + "\n")
    f.write(link + "\n\n")

    
f.write("===============================================================================\n\n")

# close the output file
f.close()
