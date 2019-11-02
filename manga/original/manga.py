from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import urllib.request
import sys
import os

# get the target url form the command line arguments
url = str(sys.argv[1])

# make the HTTP request with a custom header
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
mainHTML = urlopen(req).read()

# build the BeautifulSoup object using the html retrieved from the previous request
mainSoup = soup(mainHTML, "html.parser")

# find the chapter table and the manga name from the page
chapTable = mainSoup.find('table', {'id':'listing'})
mainName = mainSoup.find('h2',{'class':'aname'}).text

# use the contents of the chapter table to figure out the length of the manga
rows = len(chapTable.find_all('tr')) -1

# loop over the chapters in the manga using the previously found length

for issue in range(1, (rows + 1)):
	# build the chapter (issue) url out of the base url and the known format for the chapter urls
    issUrl = url + '/' + str(issue)

	# create the issue namebased on the issue index
    issueName = 'Issue' + str(issue)

	# make the HTTP request
    req = Request(issUrl, headers={'User-Agent': 'Mozilla/5.0'})
    issueHTML = urlopen(req).read()

	# build the BeautifulSoup object
    issueSoup = soup(issueHTML, 'html.parser')

	# find out how many pages exists on this chapter/issue by using the pageMenu dropdown and how many options there are to select from
    dropdown = issueSoup.find('select', {'id':'pageMenu'})

    pageCount = len(dropdown.find_all('option'))
    
	# create the directory where the data for a given chapter/issue will live in
    os.makedirs('./' + mainName + '/' + issueName, mode=0o755)

	
	# loop over the pages in a chapter/issue
    for chap in range(1, (pageCount + 1)):
		# build the page url
        pageUrl = issUrl + '/' + str(chap)


		# make the request
        req = Request(pageUrl, headers={'User-Agent': 'Mozilla/5.0'})
        pageHTML = urlopen(req).read()

		# build the BeautifulSoup object
        pageSoup = soup(pageHTML, 'html.parser')

		# find the image source url
        imgSrc = pageSoup.find('img', {'id':'img'})['src']

		# use the image source url to download the .jpg of page
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(imgSrc, './' + mainName + '/'+ issueName + '/' + str(chap) + '.jpg')

