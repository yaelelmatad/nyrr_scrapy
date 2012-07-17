# Scrapy settings for nyrr_stats project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'nyrr_stats'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['nyrr_stats.spiders']
NEWSPIDER_MODULE = 'nyrr_stats.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
FEED_FORMAT = 'csv'
