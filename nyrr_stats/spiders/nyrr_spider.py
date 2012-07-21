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
gender_age_re = re.compile('(.)([0-9]+)', re.UNICODE)
metadata_re = re.compile(r'<b>(.+?):.*?</b>(.+?)<br>',re.UNICODE)
#.+ means anything with any number of characters (+), sepearated by <br> -- any text that isn't special, r = raw string
m_raceName = "" 
m_location = ""
m_distMiles = ""
m_date = ""
m_temp = ""
m_humidity = ""
dataLocation = []

class NYRRSpider(BaseSpider):
    linkextractor = SgmlLinkExtractor("result\.id=")
    linkextractor2 = SgmlLinkExtractor("http://web2.nyrrc.org/cgi-bin/htmlos.cgi/")
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
        for x in self.linkextractor.extract_links(response)[:3]:
            req.append(Request(x.url, callback = self.parseRaces))
        return req

    def parseRaces(self, response):
        req = FormRequest.from_response(response,
            formdata = {"items.display":"500"},
            callback=self.parseRace)
        return req
    
    def parseRace(self,response):
        global m_temp
        global m_humidity
        global m_raceName
        global m_date
        global m_distMiles
        global m_location 

        hxs = HtmlXPathSelector(response)
        rn =  hxs.select('//title/text()').extract()
        m_raceName = rn[0]
        metadata = hxs.select("//span[@class='text']").extract()[0]
        parsedMetadata =  metadata_re.findall(metadata)
        for name, value in parsedMetadata:
            m_distMiles = "" #IN CASE THES DON'T EXIST IN DATA
            m_date = ""
            m_temp = ""
            m_humidity =""
            m_location = ""

            if name=='Distance':
                m_distMiles = value.split(" ")[0]

            if name=='Date/Time':
                m_date = value
    
            if name=='Weather':
                parsedWeatherUni = weather_uni_re.findall(value)
                if parsedWeatherUni:
                    m_temp = parsedWeatherUni[0]
                else: 
                    parsedWeatherDeg = weather_deg_re.findall(value)
                    if parsedWeatherDeg:
                        m_temp = parsedWeatherDeg[0]
                    else:
                        m_temp =""
                
                parsedHumidity = humidity_re.findall(value)
                if parsedHumidity:
                    m_humidity = parsedHumidity[0]
                else:
                    m_humidity = ""

            if name=='Location':
                m_location = value   

        global dataLocation
        for j in range(0,20):
            dataLocation.append(0) #zero will always be an empty string

        header = hxs.select('//table[2]/tr[1]/td[1]/text()').extract()
        i=1;

        while (header): #go through column by column
            #print header
            headerStripped = [j for j in header if j != u'\xa0'] #get rid of the garbage nbsp
            headerConcat = ' '.join(headerStripped) #concatinate
            dataLocation[(self.whichDataMember(headerConcat))]=i
            i = i + 1
            header =  hxs.select('//table[2]/tr[1]/td[' + str(i) + ']/text()').extract()
        
        runnerData = []
        for j in range(0,30):
            runnerData.append("")

        data  = hxs.select('//table[2]/tr[2]/td[1]/text()').extract()
	print data
        k = 2
        while(data):
            i=1
            while(data):
                dataStripped = [j for j in data if j != u'\xa0'] #get rid of the garbage nbsp
                dataConcat = ' '.join(dataStripped) #concatinate
                runnerData[i] = dataConcat.lower() #save all as lower case
                i = i + 1
                data =  hxs.select('//table[2]/tr[' + str(k) + ']/td[' + str(i) + ']/text()').extract()
		print data
				
            #need to split up gender age data
            genderAge = gender_age_re.findall(runnerData[dataLocation[3]])
            m_gender = genderAge[0][0]
            m_age = genderAge[0][1]

            item = NyrrStatsItem(raceName = rn[0].lower(), location=m_location.lower(), distMiles = m_distMiles.lower(), date = m_date.lower(), temp = m_temp.lower(), 
                        humidity = m_humidity.lower(),
                        lastName = runnerData[dataLocation[1]],
                        firstName = runnerData[dataLocation[2]],
                        sex = m_gender,
                        age = m_age,
                        bib = runnerData[dataLocation[4]],
                        team = runnerData[dataLocation[5]],
                        city = runnerData[dataLocation[6]],
                        state = runnerData[dataLocation[7]],
                        country = runnerData[dataLocation[8]],
                        overallPlace= runnerData[dataLocation[9]],
                        genderPlace= runnerData[dataLocation[10]],
                        agePlace= runnerData[dataLocation[11]],
                        netTime= runnerData[dataLocation[12]],
                        pacePerMile= runnerData[dataLocation[13]],
                        AGTime= runnerData[dataLocation[14]],
                        AGGenderPlace= runnerData[dataLocation[15]],
                        AGPercent= runnerData[dataLocation[16]],
                        )
            yield item

            k = k + 1
            data =  hxs.select('//table[2]/tr[' + str(k) + ']/td[1]/text()').extract()
	    print data


        #parseRunnersReturned = self.parseRunners(response)
        return 
        #return parseRunnersReturned + [item]
    
    
    
    def parseRunners(self, response):
        req = []
        for x in self.linkextractor2.extract_links(response):
            print x.text
            if (x.text =='NEXT 500'):
                print m_raceName
                req.append(Request(x.url, callback = self.parseRunners))
                parsedOnePageReturned = self.parseOnePageRunner(response)                
                break 
        
        return [req] + parsedOnePageReturned

    def parseOnePageRunner(self, response):
        print dataLocation
        print m_raceName
        hxs = HtmlXPathSelector(response)
        runnerData = []
        for j in range(0,30):
            runnerData.append("")

        data  = hxs.select('//table[2]/tr[2]/td[1]/text()').extract()
        k = 2
        while(data):
            i=1
            while(data):
                dataStripped = [j for j in data if j != u'\xa0'] #get rid of the garbage nbsp
                dataConcat = ' '.join(dataStripped) #concatinate
                runnerData[i] = dataConcat.lower() #save all as lower case
                i = i + 1
                data =  hxs.select('//table[2]/tr[' + str(k) + ']/td[' + str(i) + ']/text()').extract()

                #need to split up gender age data
            if (runnerData[dataLocation[3]]):
                genderAge = gender_age_re.findall(runnerData[dataLocation[3]])
                m_gender = genderAge[0][0]
                m_age = genderAge[0][1]

            item = NyrrStatsItem(raceName = rn[0].lower(), location=m_location.lower(), distMiles = m_distMiles.lower(), date = m_date.lower(), temp = m_temp.lower(), 
                        humidity = m_humidity.lower(),
                        lastName = runnerData[dataLocation[1]],
                        firstName = runnerData[dataLocation[2]],
                        sex = m_gender,
                        age = m_age,
                        bib = runnerData[dataLocation[4]],
                        team = runnerData[dataLocation[5]],
                        city = runnerData[dataLocation[6]],
                        state = runnerData[dataLocation[7]],
                        country = runnerData[dataLocation[8]],
                        overallPlace= runnerData[dataLocation[9]],
                        genderPlace= runnerData[dataLocation[10]],
                        agePlace= runnerData[dataLocation[11]],
                        netTime= runnerData[dataLocation[12]],
                        pacePerMile= runnerData[dataLocation[13]],
                        AGTime= runnerData[dataLocation[14]],
                        AGGenderPlace= runnerData[dataLocation[15]],
                        AGPercent= runnerData[dataLocation[16]],
                        )
            k = k + 1
            data =  hxs.select('//table[2]/tr[' + str(k) + ']/td[1]/text()').extract()

        return [item]

    def whichDataMember(self, member):
        myDict = {'Last Name': 1,
                'First Name': 2,
                'Sex/ Age': 3,
                'Bib':4,
                'Team': 5,
                'City':6,
                'State':7,
                'Country':8,
                'Overall Place':9,
                'Gender Place':10,
                'Age Place':11,
                'Net Time':12,
                'Finish Time':12,
                'Pace/ Mile':13,
                'AG Time':14,
                'AG Gender Place':15,
                'AG %':16}

        if(member in myDict):
            return myDict[member]
        else:
            return -1

    #want to do something like this
    #food = 'bread'
    #vars()[food] = 123
    #print bread  # --> 123
