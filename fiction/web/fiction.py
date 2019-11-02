#! /usr/local/bin/python3.7

from bs4 import BeautifulSoup as soup
import urllib.request
import sys
import os
from requests_html import HTMLSession

# get the target url form the command line arguments
url = str(sys.argv[1])

# for any given fanfiction.net link only the first 5 parts matter for location a story
# https://www.fanfiction.net/s/8897431/1/Child-of-the-Storm				--> Original
# https: | | www.fanfiction.net | s | 8897431 | 1 | Child-of-the-Storm	--> Post Split (| represent the places where the split occurred
# https://www.fanfiction.net/s/8897431 									--> rebuilt URL
split = url.split('/')
main = split[0] + "/" + split[1] + '/' + split[2] + '/' + split[3]+ '/' + split[4]

# Create the session object
session = HTMLSession()

# send a GET HTTP request
pageHTML = session.get(main)

# render() load the html into a headless pupeteer browser and executes any javascript on the page (this is important because parts of the page a dynamically loaded using JQuery)
pageHTML.html.render()

# build the BeautifulSoup object based on the now rendered HTML
pageSoup = soup(pageHTML.html.html, "html.parser")

# create the directory where the story will live based on the name of the story
dirName = '/var/www/flaskapps/optionone/fictions/' +  pageSoup.find('b',{'class':'xcontrast_txt'}).text
os.mkdir(dirName)

# create a link to a local copy of the stylesheet that will be retrieved later
styleSheets = '<link rel="stylesheet" href="./xss26.css">'

# find the length of the storyy based on the existance of a known select tag. If the tag does not exists the story has 1 chapter only
length = 1
dropdown = pageSoup.find('select', {'id':'chap_select'})
if dropdown is not None:
        length = len(dropdown.findAll('option'))

# boolean flag used later
first = True

# loop over the chapters in the story
for chap in range(1, (length + 1)):
	# build the chapter URL based on the original URL and the know chapter index
    chapURL = main + "/" + str(chap)

	# retrieve and render the HTML data
    chapHTML = session.get(chapURL)
    chapHTML.html.render()
	
	# build the BeautifulSoup object
    chapSoup = soup(chapHTML.html.html, "html.parser")

	# open the file in which this particular chapter will be written
    f = open(dirName +"/Chapter " + str(chap) + ".htm", "w")

	# find any existing style tags in the original HTML doc and save them to a variable
    style = ''
    for i in chapSoup('style'):
        style += str(i)

	# find the body tag of the document
    chapBody = chapSoup.body

	# find the specific div in the body that actually contains the story text
	# there are others divs in the doby, but those are used for parts of the page that do no interest me
    chapStory = chapBody.find('div', {'id':'content_parent'})

	# retrieve the profile image URL from the src attribute of the img tag
    profImgURL = chapStory.find('div', {'id': 'profile_top'}).find('img', {'class':'cimage'})['src']

	# change the src tag of the profile image to point to a local copy of the img (this local copy will be retrieved later)
    chapStory.find('div', {'id': 'profile_top'}).find('img', {'class':'cimage'})['src'] = "./profImg.jpg"

    # delete uneeded tags (these are sections of the page that deal with:
		# reviews
		# favorites
		# report
		# font up/down
		# reading width up/down
		# headers and footers 
		# etc
    chapStory.find('div', {'id':'img_large'}).decompose()
    chapStory.find('div', {'id':'pre_story_links'}).decompose()
    for div in chapStory.find_all('div', {'class':'lc-wrapper'}):
        div.decompose()

	# remove any embedded scripts now that they have ran and are no longer of use
    for sc in (chapStory('script')):
        sc.decompose()

    chapStory.find('button', {'class':'btn pull-right icon-heart'}).decompose()
    
    # removing outbound links by replacing them with # for their href attribute
    chapStory.find('div', {'id':'review'}).decompose()
    for a in chapStory.find_all('a', {'class':'xcontrast_txt'}):
        a['href'] = "#"

    chapStory.find('span',{'class':'xgray xcontrast_txt'})('a')[1]['href']="#"

    # adjusting the select dropdown so that they point to the local html files
    for dropdown in (chapStory.find_all('select', {'id':'chap_select'})):
        dropdown['onChange'] = "self.location = './Chapter '+ this.options[this.selectedIndex].value + '.htm';"    

	# adjusting the next chapter/previous chapter buttons to point to the right place
    for btn in (chapStory.find_all('button', {'class':'btn'})):
        if (btn.text == "Next >"):
            btn['onClick'] = "self.location='Chapter "  + str(chap + 1) + ".htm'"
        elif (btn.text == "< Prev"):
            btn['onClick'] = "self.location='Chapter " + str(chap - 1) + ".htm'"
    

    # get profile img and hardcopy stylesheet using the boolean flag from before to ensure it only happens once
    if (first):
        if (profImgURL != None):
            urllib.request.urlretrieve('https:' + profImgURL, './' + dirName + '/profImg.jpg')
        urllib.request.urlretrieve('https://www.fanfiction.net/static/styles/xss26.css', './' + dirName + '/xss26.css')
        first = False
		
	# start building the output HTML string by combining the style tags just saved to a variable and the previously written local style-sheet link along with the chapStory variable
    html = "<html>\n<head>\n" + str(style) + "\n" + styleSheets + "<style>\np{font-size:18}\n.storytextp{margin-right:120px;margin-left:120px}\n</style>\n</head>\n<body>\n" + str(chapStory) + "</body>\n</html>"

	# write the data out to a file and close it
    f.write(html)
    f.close

# print the name of the generated directory to stdout so that it can be used by ficHandler.py
print(dirName, end="")

