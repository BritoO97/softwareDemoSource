This is the original version of the scraper created to scrape a daily report froma variety of websites<br>
Written for Python 3 and will not work in Python 2 because of package name differences<br>
Written during my last year of college as a way to introduce myself to linux environments and because i like to keep on top of the latest game releases and special discounts<br>

The daily report will consists of 3 sections:<br>
    Weather forecast for the day<br>
    Current top 25 special deals on Steam<br>
    Current top 25 special deals on GOG<br>

Usage:<br>
    The scripts are never ran directly. Instead a handler bash script is used<br>

    #!/bin/bash

    location=$(dirname $0)
    cd $location

    rm results
    echo "starting" >> log

    echo "Table Of Contents" >> results
    echo "   1. Weather" >> results
    echo "   2. Steam" >> results
    echo "   3. GOG" >> results
    echo "" >> results

    /usr/bin/python3 weather.py
    /usr/bin/python3 steamScraper.py
    /usr/bin/python3 gogScraper.py
    /usr/bin/python3 emailer.py
    echo "ending" >> log

The runner script changes the PWD to the correct location, removes the previous day's results, echo's a quick table of contents to the results file and calls each of the scrapers in turn<br>

Finaly the runner script is set to run every dat a 8:00 AM Eastern Time using a cronjob (0 8 * * * /bin/bash ~/TestScraper/runner)<br>

Output:<br>
    There is no direct output, intead an email is sent to whoever is listed in the to variable of the emailer script
