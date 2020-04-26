# A web scraper for myauto.ge - the largest car buying and selling website.
###### Crawls and extracts data from each announcement, data contains car characteristics and images.

Used framework and libraries:
1. **Scrapy** - for crawling and extracting data
2. **Beautiful Soup** - for html parsing and extracting data

How to run:
1. *python -m scrapy crawl myauto -o _temp_files/features_temp.csv*
2. *python images_downloader.py*

By default, it pulls the first 10 pages from myauto, that's because there are thousands of pages and needs lots of time to finish. You can change it on 8th line in myauto.py spider file

Result files:
1. features.csv - car characteristics
2. images folder - car images 