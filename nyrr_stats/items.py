# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class NyrrStatsItem(Item):
    # define the fields for your item here like:
    raceName = Field()
    distMiles = Field()
    date = Field()
    temp = Field()
    location = Field()
    humidity = Field()
    lastName = Field()
    firstName  = Field()
    sex = Field()
    age  = Field()
    bib  = Field()
    team  = Field()
    city = Field()
    state = Field()
    country  = Field()
    overallPlace  = Field()
    genderPlace = Field()
    agePlace = Field()
    netTime  = Field()
    pacePerMile = Field()
    AGTime = Field()
    AGGenderPlace  = Field()
    AGPercent  = Field()
    pass


