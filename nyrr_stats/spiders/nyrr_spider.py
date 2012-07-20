from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import re
#from BeautifulSoup import BeautifulSoup
from nyrr_stats.items import NyrrStatsItem

humidity_re = re.compile(r'([0-9]+)%',re.UNICODE)
weather_deg_re = re.compile(r'([0-9]+)? [Dd]eg', re.UNICODE)
weather_uni_re = re.compile(',+? ([0-9]+).*?F', re.UNICODE)
#weather_re = re.compile(r'([0-9]+) ?[Dd]eg|\\xb0F',re.UNICODE)
metadata_re = re.compile(r'<b>(.+?):.*?</b>(.+?)<br>',re.UNICODE)
#.+ means anything with any number of characters (+), sepearated by <br> -- any text that isn't special, r = raw string
class NYRRSpider(BaseSpider):
    linkextractor = SgmlLinkExtractor("result\.id=")
    name = "nyrr"
    allowed_domains = ["web2.nyrrc.org"]
    start_urls = [
        "http://web2.nyrrc.org/cgi-bin/start.cgi/aes-programs/results/resultsarchive.htm",
    ]
    
    def parse(self, response):
        req = []
        for i in range(2007,2008):
            req.append(FormRequest.from_response(response,
                formdata = {"NYRRYEAR":str(i)}, 
                callback=self.parse2))
        
        return req;

    def parse2(self, response): 
        req=[]
        #for x in self.linkextractor.extract_links(response):
        for x in self.linkextractor.extract_links(response)[:40]:
            req.append(Request(x.url, callback = self.parseRaces))
        return req

    def parseRaces(self, response):
        req = FormRequest.from_response(response,
            formdata = {"items.display":"500"},
            callback=self.parseRace)
        return req
    
    def parseRace(self,response):
        hxs = HtmlXPathSelector(response)
        rn =  hxs.select('//title/text()').extract()
        metadata = hxs.select("//span[@class='text']").extract()[0]
        parsedMetadata =  metadata_re.findall(metadata)
        #print parsedMetadata
        #for name, value in parsedMetadata:
            #name.encode('ascii', 'replace')
            #value.encode('ascii', 'replace')
            #name = str(name)
            #value = str(value)
            #name.replace(u'\\xa0',u'')
            #print name
            #print value

        #print parsedMetadata
        for name, value in parsedMetadata:
            if name=='Distance':
                m_distMiles = value.split(" ")[0]
                #print "Distance = ", raceDistMiles

            if name=='Date/Time':
                m_date = value
                #print "Date Time = " + dateTime
    
            if name=='Weather':
                #print "value " + value
                parsedWeatherUni = weather_uni_re.findall(value)
                if parsedWeatherUni:
                    m_temp = parsedWeatherUni[0]
                else: 
                    parsedWeatherDeg = weather_deg_re.findall(value)
                    if parsedWeatherDeg:
                        m_temp = parsedWeatherDeg[0]
                    else:
                        m_temp =""

                #print temp
                
                parsedHumidity = humidity_re.findall(value)
                if parsedHumidity:
                    m_humidity = parsedHumidity[0]
                else:
                    m_humidity = ""

            if name=='Location':
                m_location = value   

        header = hxs.select('//table[2]/tr[1]/td[1]/text()').extract()
        i=1;
        while (header):
            #print header
            headerStripped = [j for j in header if j != u'\xa0']
            headerConcat = ' '.join(headerStripped)
            print self.whichDataMember(headerConcat)
            print headerConcat
            i = i + 1
            header =  hxs.select('//table[2]/tr[1]/td[' + str(i) + ']/text()').extract()
        

        item = NyrrStatsItem(raceName = rn[0], location=m_location, distMiles = m_distMiles, date = m_date, temp = m_temp, humidity = m_humidity)
        return [item]


    def whichDataMember(self, member):
        if (member == 'Last Name'):
            return 'lastName'

        if (member == 'First Name'):
            return 'firstName'

        if (member == 'Sex/ Age'):
            return 'sexAge'

        if (member == 'Bib'):
            return 'bib'

        if (member == 'Team'):
            return 'team'

        if (member == 'City'):
            return 'city'

        if (member == 'State'):
            return 'state'

        if (member == 'Country'):
            return 'country'

        if(member == 'Overall Place'):
            return 'overallPlace'

        if(member == 'Gender Place'):
            return 'genderPlace'

        if(member == 'Age Place'):
            return 'agePlace'

        if(member == 'Net Time'):
            return 'netTime'

        if(member == 'Finish Time'):
            return 'netTime' #note for pre timing chip races we'll take this to be the finish time.

        if(member == 'Pace/ Mile'):
            return 'pacePerMile'

        if(member == 'AG Time'):
            return 'AGTime'

        if(member == 'AG Gender Place'):
            return 'AGGenderPlace'

        if(member == 'AG %'):
            return 'AGPercent'

        return 'NotTracked'


    #want to do something like this
    #food = 'bread'
    #vars()[food] = 123
    #print bread  # --> 123
