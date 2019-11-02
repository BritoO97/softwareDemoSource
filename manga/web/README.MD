This is the web demo of the scraper created to scrape mangas from mangareader.net at the request of a friend who loved to read, but hated the website<br>
Written for Python 2 because of Flask and modwsgi<br>

Differences:<br>
	The main differences between this version and the original are the fact that the code and packages used had to be downgraded to work with Python 2. Because of some differences between how python handles strings between Py2 and Py3 a few explicit encoding and decoding had to be added<br>
	This version only retrieves the first 3 pages of the first 3 chapter because of the time complexity of the full operation.<br>
	It also does not write the images to file, instead returning the image source URL to the client page where is it used to dynamically display the pages.<br>

Output:<br>
	A list of image source URL's.<br>
