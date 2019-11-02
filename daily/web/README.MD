This is the version of the scraper created to work with the web demo page<br>
Written for Python 2 because of Flask and modwsgi<br>

The daily report will consists of 3 sections:<br>
    Weather forecast for the day<br>
    Current top 25 special deals on Steam<br>
    Current top 25 special deals on GOG<br>

Differences:<br>
	The main differences between this version and the original are the fact that the code and packages used had to be downgraded to work with Python 2. Because of some differences between how python handles strings between Py2 and Py3 a few explicit encoding and decoding had to be added<br>

Output:<br>
    An email is sent to whoever is listed in the dest variable of the emailer function.<br>
	A copy of the data is also returned to the client page
