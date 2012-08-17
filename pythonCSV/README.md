Here are two "cleaners" for the data retrieved by the nyrr scrapy spiders.

The first one is csvEditor.py which is a script that converts the results of the scraping to useful mysql types.  Converts all running times to seconds.  Also converts dates to YY-MM-DD 00:00:00.  Races without time will be given a start time of 6am.

The second one is memEditor.py which is a script that converts the results of the scraping to useful mysql types.  Converts all running times to seconds. Also converts dates to YY-MM-DD 06:00:00 (note since there are not start times for member data they are automatically given 6am start times).

Running the scripts is as follows:

python scriptname.py input.csv > output.csv

Note, that you may still need to do some search and replace for regularizing the data.  
To deal with ampersands run the following command (in vi)
(global delate of amp: leaving the & character)

:%s/amp;//g  
