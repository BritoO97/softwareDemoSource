This is the original version of the scraper created to scrape mangas from mangareader.net at the request of a friend who loved to read, but hated the website<br>
Written for Python 3 and will not work in Python 2 because of package name differences<br>

Usage (in a bash terminal):<br>
    python3 manga.py url

where url will be a url in the format of "https://www.mangareader.net/naruto"<br>

Output:<br>
The results of running this script is a folder named after the manga being scraped<br>
This folder will contain more subfolders, one for each issue/chapter of the manga<br>
Each subfolder will contain a series of .jpg images, numbered 1 to n (n being the number of pages in a particular issue)<br>

If the sample URL given above is used the result will be as follow<br>

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


NOTE: Linux systems will list the directory contents in alphabetical order by default, meaning that you might see something like this:<br>
10.jpg<br>
11.jpg<br>
12.jpg<br>
...<br>
19.jpg<br>
1.jpg<br>
20.jpg<br>
21.jpg<br>
...<br>
29.jpg<br>
2.jpg<br>
...<br>

In a windows system the ordering will be:<br>
1.jpg<br>
2.jpg<br>
...<br>
10.jpg<br>
11.jpg<br>
...<br>
20.jpg<br>
21.jpg<br>
...<br>

which is the desired goal<br>