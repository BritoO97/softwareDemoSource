from bs4 import BeautifulSoup as soup
from urllib2 import Request, urlopen
import urllib2

def start(url):

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

	# prepare the list which will end up hoilding the final url links
    linkList = []

	# if a story has less than 3 chapters use that number instead of 3 (4 is used because the range function goes up to, but does not include the 2nd parameter)
    ln = 4

    if (rows < 4):
        ln = rows

	# loop over the first 3 (or less) chapters
    for issue in range(1,ln):
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
        
		# much like before i am only interested in the first 3 (or less) pages of a chapter
        inLn = 4

        if (pageCount < 4):
            inLn = pageCount + 1

		# loop over the pages in a chapter/issue
        for chap in range(1,inLn):
			# build the page url
            pageUrl = issUrl + '/' + str(chap)

            # make the request
			req = Request(pageUrl, headers={'User-Agent': 'Mozilla/5.0'})
            pageHTML = urlopen(req).read()

            # build the BeautifulSoup object
			pageSoup = soup(pageHTML, 'html.parser')

			# find the image source url
            imgSrc = pageSoup.find('img', {'id':'img'})['src']

			# add the image source url to the list
            linkList.append(imgSrc)

	# return the contents of the list
    return linkList
