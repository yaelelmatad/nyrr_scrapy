from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import re
from nyrr_stats.items import NyrrMemberStatsItem

metadata_re = re.compile(r'<b>(.+?)</b><br>(.+?)</td>',re.UNICODE)
name_re = re.compile(r'colspan="2">(.+?), (.+?) .+? ([0-9]+)</td>',re.UNICODE)
details_re =re.compile(r'<b>(.+?):</b></td><td class="text">(.+?)</td>',re.UNICODE)
data_re = re.compile(r'(.+?)\xa0',re.UNICODE)
place_re = re.compile(r'([0-9]+).+?([0-9]+)',re.UNICODE) 

#.+ means anything with any number of characters (+), sepearated by <br> -- any text that isn't special, r = raw string

class NYRRSpider(BaseSpider):
    #linkextractor = SgmlLinkExtractor("result\.id=")
    linkextractor2 = SgmlLinkExtractor("http://web2.nyrrc.org/cgi-bin/htmlos.cgi/")
    name = "nyrrmembers"
    allowed_domains = ["web2.nyrrc.org"]
    start_urls = [
         "http://web2.nyrrc.org/cgi-bin/start.cgi/aes-programs/results/members/member_history.html",
    ]

    def parse(self, response):
        req = []
        #for i in range(104136,104137): 
        for i in range(1,140001):
            req.append(FormRequest.from_response(response,
                formdata = {"MEMNUMBER":str(i)}, 
                callback=self.parse2))
        return req;

    def parse2(self, response): 
        req=[]
#        for i in range (2008,2009):
        for i in range(1991,2013):
            req.append(FormRequest.from_response(response,
                formdata = {"MEMYEAR":str(i)}, 
                callback=self.parseRace)) 
        return req

    def parseRace(self, response): 
        item = []
        req = []
        hxs = HtmlXPathSelector(response)
        try:
            name = hxs.select("//table[1]").extract()
            parsedName = name_re.findall(name[0])
            m_lastName = parsedName[0][0]
            m_firstName = parsedName[0][1]
        except:
            return req + item

        parsedDetails = details_re.findall(name[0])
        m_memberNumber = parsedDetails[0][1]

        #now actually parse the race table
        
        header = hxs.select('//table[2]/tr[1]/td[1]/text()').extract()
        dataLocation = []
        for i in range (0,20):
            dataLocation.append(0)
       
        numColumns = 1
        i = 1
        m_raceName = ""
        m_raceData = ""
        while (header): #go through column by column
            if header[2] == "(miles)":
                headerConcat = 'dist'
            else:
                headerStripped = [j for j in header if j != u'\xa0'] #get rid of the garbage nbsp
                headerConcat = ' '.join(headerStripped) #concatninate
            dataLocation[(self.whichDataMember(headerConcat))]=i
            i = i + 1
            numColumns = i
            header =  hxs.select('//table[2]/tr[1]/td[' + str(i) + ']/text()').extract()
            

        runnerData = []
        for j in range(0,30):
            runnerData.append("")

        data  = hxs.select('//table[2]/tr[2]/td[1]').extract()
        k = 2 #second row starts actual data
        while(data):
            try:
                data_re=metadata_re.findall(data[-1])
            except:
                try:
                    data_re=metadata_re.findall(data[0])
                except:
                    #print "exception"
                    #print data
                    return req + item
            try:
                m_raceName = data_re[0][0].lower()
                m_raceDate = data_re[0][1].lower()
            except:
                #print data
                #print 
                #print "exception rn,  rd"
                #print data_re
                return req + item


            save = 1
            for i in range (2, numColumns):
                data =  hxs.select('//table[2]/tr[' + str(k) + ']/td[' + str(i) + ']/text()').extract()
                #print data
                if data[0] and 'MQ' in data[0] or 'VQ' in data[0]:
                    #print "marathon/volunteer Q , break"
                    save = -1
                    break
                
                temp = data[-1]
                #print data
                try:
                    while len(temp)> 0 and u'\xa0' in temp:
                        temp  = temp[:-1]
                except:
                    temp =""
                    #print "exception"
                #print temp

                runnerData[i] = temp.lower()

            if save == 1:
                m_gender =""
                if dataLocation[7]>0:
                    m_gender = 'm'
                    try:
                       genderPlacere = place_re.findall(runnerData[dataLocation[7]])
                       m_genderPlace = genderPlacere[0][0]
                       m_totalOfGender = genderPlacere[0][1]
                    except:
                        m_genderPlace = ""
                        m_totalOfGender = ""
                elif dataLocation[8]>0:
                    m_gender = 'f'
                    try:
                       genderPlacere = place_re.findall(runnerData[dataLocation[8]])
                       m_genderPlace = genderPlacere[0][0]
                       m_totalOfGender = genderPlacere[0][1]
                    except:
                        m_genderPlace = ""
                        m_totalOfGender = ""
                else:
                    "no gender?"
                    m_gender = ""
                    m_genderPlace =""
                    m_totalOfGender = ""
                    
                try:
                    agePlacere = place_re.findall(runnerData[dataLocation[9]])
                    m_agePlace = agePlacere[0][0]
                    m_totalOfAge = agePlacere[0][1]
                except:
                    m_agePlace = ""
                    m_totalOfAge = ""
                
                try:
                    overallPlacere=place_re.findall(runnerData[dataLocation[6]])
                    m_overallPlace=overallPlacere[0][0]
                    m_totalRunners=overallPlacere[0][1]
                except:
                    m_overallPlace = ""
                    m_totalRunners = ""

                if runnerData[dataLocation[5]] != "": #weirdness with duplicates w/o netTime?
                    item.append(NyrrMemberStatsItem(raceName = m_raceName.lower(), 
                        distMiles = runnerData[dataLocation[2]].lower(), 
                        date = m_raceDate.lower(),
                        lastName = m_lastName.lower(),
                        firstName = m_firstName.lower(),
                        memberNumber = m_memberNumber.lower(),
                        sex = m_gender.lower(),
                        overallPlace= m_overallPlace.lower(),
                        totalRunners = m_totalRunners.lower(),
                        genderPlace= m_genderPlace.lower(),
                        totalOfGender = m_totalOfGender.lower(),
                        agePlace= m_agePlace.lower(),
                        totalOfAge = m_totalOfAge.lower(),
                        netTime= runnerData[dataLocation[4]].lower(),
                        pacePerMile= runnerData[dataLocation[5]].lower(),
                        AGTime= runnerData[dataLocation[10]].lower(),
                        PerfPercent = runnerData[dataLocation[11]].lower(),
                        ))

            k = k + 1
            data =  hxs.select('//table[2]/tr[' + str(k) + ']/td[1]').extract()
            
        return item + req
    
    def whichDataMember(self, member):
        myDict = {'Race Name, Date': 1,
                'dist': 2,
                'Gun Time': 3,
                'Net Time': 4,
                'Pace per Mile': 5,
                'Overall Place/ Total Finishers':6,
                'Gender Place/ Total Males':7,
                'Gender Place/ Total Females':8,
                'Age Place/ Total in Age Grp.':9,
                'Age-Grd. Time':10,
                'Perf. %':11,
                }
        if(member in myDict):
            return myDict[member]
        else:
            return -1

