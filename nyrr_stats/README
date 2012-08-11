This is a python based web scraper for the nyrr race data webpage.

the nyrr_spider spider scrapes all the race pages including details about race such as location and weather conditions
It will scrape the data up until the end of year 2012 (change the spider/nyrr_spider.py file to go further)

the nyrr_members_spider scrapes all the data for specific member numbers.  This allows you to group results by the NYRR member ID number.

Using these scrapers requires scrapy (a python web scraper framework):
http://scrapy.org/

These processes can be quite slow.  Scraping the race database took ~12 hours on a macbook pro on a wireless connection.  Requests seem to be the bottle neck.

Useful commands to run nyrr_spider:
Note: items.csv is your target csv file (but you can change the file name)

verbose mode:
scrapy crawl nyrr --set FEED_URI=items.csv --set FEED_FORMAT=csv

production mode:
scrapy crawl -L CRITICAL --logfile=logfile.log nyrr --set FEED_URI=items.csv --set FEED_FORMAT=csv > output

Useful commands to run nyrr_members_spider
verbose mode:
scrapy crawl nyrrmembers --set FEED_URI=items.csv --set FEED_FORMAT=csv

production mode:
scrapy crawl -L CRITICAL --logfile=logfile.log nyrrmembers --set FEED_URI=items.csv --set FEED_FORMAT=csv > output

Once scraped it is useful to run the python "clean up"  tool also located in this library --  csvCleaner.py.
use as follows:
python csvCleaner.py rawcsvfilename > cleanedupcsvfilename
