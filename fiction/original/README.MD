This is the original version of the scraper created to scrape fanfictions from fanfiction.net to be able to archive them for later reading<br>
Written for Python 3.6 or 3.7 and will not work in earlier version due to the request_html package<br>

Usage (in a bash terminal):<br>

	python3.7 fiction.py url

where url will be a url in the format of "https://www.fanfiction.net/s/2630300/1/You-Did-What" or "https://www.fanfiction.net/s/2630300/1" or "https://www.fanfiction.net/s/2630300"<br>
The first number after the 's' must be part of the URL. Anything after is optional since the script will rebuild the URL down to "https://www.fanfiction.net/s/2630300"<br>

Output:<br>
The results of running this script is a folder named after the fiction being scraped<br>
This folder will contain one .htm file for each chapter in the story and .jpg file for the profile image and a .css file for the local copy of the style sheet<br>

Is the sample URL given above is used the result will be as follow<br>

	.
	├── fiction.py
	└── You Did What!
		├── Chapter 10.htm
		├── Chapter 11.htm
		├── Chapter 12.htm
		├── Chapter 13.htm
		├── Chapter 14.htm
		├── Chapter 15.htm
		├── Chapter 16.htm
		├── Chapter 17.htm
		├── Chapter 18.htm
		├── Chapter 19.htm
		├── Chapter 1.htm
		├── Chapter 20.htm
		├── Chapter 21.htm
		├── Chapter 2.htm
		├── Chapter 3.htm
		├── Chapter 4.htm
		├── Chapter 5.htm
		├── Chapter 6.htm
		├── Chapter 7.htm
		├── Chapter 8.htm
		├── Chapter 9.htm
		├── profImg.jpg
		└── xss26.css
		
NOTE: while the ordering of the chapters seems off, it does not actually matter when reading the story in a web browser<br>
