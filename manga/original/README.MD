This is the original version of the scraper created to scrape mangas from mangareader.net at the request of a friend who loved to read, but hated the website
Written for Python 3 and will not work in Python 2 because of package name differences

Usage (in a bash terminal):
    python3 manga.py url

    where url will be a url in the format of "https://www.mangareader.net/naruto"

Output:
    The results of running this script is a folder named after the manga being scraped
    This folder will contain more subfolders, one for each issue/chapter of the manga
    Each subfolder will contain a series of .jpg images, numbered 1 to n (n being the number of pages in a particular issue)

    Is the sample URL given above is used the result will be as follow

    ./
    ├── manga.py
    └── Naruto
        ├── Issue1
        │   ├── 1.jpg
        │   ├── 2.jpg
        │   ├── 3.jpg
        │   ├── 4.jpg
        │   ├── 5.jpg
        │   ├── ...
        │   
        ├── Issue2
        │   ├── 1.jpg
        │   ├── 2.jpg
        │   ├── 3.jpg
        │   ├── 4.jpg
        │   ├── 5.jpg
        │   ├── ...
        │
        ├── ...


        NOTE: Linux systems will list the directory contents in alphabetical order by default, meaning that you might see something like this:
            10.jpg
            11.jpg
            12.jpg
            ...
            19.jpg
            1.jpg
            20.jpg
            21.jpg
            ...
            29.jpg
            2.jpg
            ...

        In a windows system the orderign will be:
            1.jpg
            2.jpg
            ...
            10.jpg
            11.jpg
            ...
            20.jpg
            21.jpg
            ...

        which is the desired goal