from bs4 import BeautifulSoup as soup
from urllib2 import Request, urlopen
import json
#import codec
from io import open
import smtplib
from email.mime.text import MIMEText
import os

# hardcoded file to which report is written to
filename = '/var/www/flaskapps/optionone/results'

# function called from the flask rest api, which take in a target email and runs all subbsequest part of the daily reporter
def start(dest):
    # ensures that a previous version of the report does not exists, should something have happened in the previous iteration of the tool that would prevent its deletion
    if (os.path.exists(filename)):
        os.remove(filename)
    
    # call each part of the daily reporter
    weather();
    steam();
    gog();

    # Read back the generated report and send to email function
    fi = open(filename, 'r', encoding='utf-8');
    data = fi.read();

    email(data, dest)

    fi.close()

    # delete the report file
    if (os.path.exists(filename)):
        os.remove(filename)

    return data;

def weather():
    # hardcoded url from which to scrape
    url ="https://weather.com/weather/tenday/l/USNJ0355:1:US"

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
    with open(filename, 'a+', encoding='utf-8') as f:
    
        # write the data out to a file with some formating
        f.write(("WEATHER FORECAST\n\n").decode('utf-8'))

        f.write(("Description: " + desc.encode('utf-8') + "\nTemp: " + tempLow.encode('utf-8')  + " / " + tempHigh.encode('utf-8')  + "\nRain/Snow: " + prec.encode('utf-8')  + "\nHumidity: " + hum.encode('utf-8')  + "\n\n===================================================================================\n\n").decode('utf-8'))

def steam():
    # hardcoded url from which to scrape
    url = "https://store.steampowered.com/search/?specials=1"

    # make the HTTP request and get the HTML data
    client = urlopen(url)
    pageHTML = client.read()
    client.close()

    # build the BeautifulSoup object from the read html
    pageSoup = soup(pageHTML, "html.parser")

    # find all of the table rown we are looking for by finding the a tag that they all contain and which contains all necessary data
    itemList = pageSoup.findAll("a", {"class":"search_result_row"})

    # open the output file in append mode
    with open(filename, 'a+', encoding='utf-8') as f:
        f.write(("STEAM SPECIALS\n\n").decode('utf-8'))
        for item in itemList:

            # wrap the search in a try/except block so that if any info is missing (causing a null pointer) the offending item is ignored and the loop moves to its next iteration
            try:
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
            except:
                continue

            # write data out to the output file
            # if code execution reaches this point then all infow as found with no exceptions being thrown
            f.write((name.encode('utf-8')  + " | " + review.encode('utf-8')  + "\n" + discount.encode('utf-8')  + "\n" + oldPrice.encode('utf-8')  + " --> " + newPrice.encode('utf-8')  + "\n" + link.encode('utf-8')  + "\n\n").decode('utf-8'))

        f.write(("===============================================================================\n\n").decode('utf-8'))

def gog():
    # hardcoded url from which to scrape
    url = "https://www.gog.com/games/ajax/filtered?mediaType=game&page=1&price=discounted&sort=popularity"

    # make the HTTP request and read the JSON data
    client = urlopen(url)
    pageJSON = json.loads(client.read().decode("utf-8"))
    client.close()

    # find the item list
    products = pageJSON["products"]

    # open the output file in append mode
    with open(filename, 'a+', encoding='utf-8') as f:
        f.write(("GOG SPECIALS\n\n").decode('utf-8'))
        for i in range(0,25): 
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
            f.write((name.encode('utf-8')  + " | " + str(score).encode('utf-8') + "%\n").decode('utf-8'))
            f.write(("-" + str(discount).encode('utf-8') + "%\n").decode('utf-8'))
            f.write(("$" + str(regPrice).encode('utf-8') + " --> $" + str(newPrice).encode('utf-8') + "\n").decode('utf-8'))
            f.write((link.encode('utf-8') + "\n\n").decode('utf-8'))

        f.write(("===============================================================================\n\n").decode('utf-8'))


def email(data, dest):

# NOTE: SMTP LOGIN PASSWORD HAS BEEN REDACTED FROM THIS SCRIPT FOR PRIVACY AND SECURITY
#         IT WILL NOT WORK WITHOUT IT

    msg = MIMEText(data.encode('utf-8'))

    # email subject line
    msg['Subject'] = 'Daily Report'
    
    # Sender email (from)
    msg['From'] = 'homeserveranderson2@gmail.com'
    
    # destination email (to)
    msg['To'] = dest

    # gmail smtp server credentials
    gmailSender = "homeserveranderson2@gmail.com"
    gmailPass = "REDACTED"

    # establish connection to the smtp server
    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.ehlo()
    server.starttls()
    server.ehlo()
    
    # login to the server
    server.login(gmailSender, gmailPass)

    # send the email
    server.sendmail(gmailSender, [dest], msg.as_string())

    # close connection
    server.quit()
