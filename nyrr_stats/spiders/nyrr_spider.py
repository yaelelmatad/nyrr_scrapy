from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import re
from nyrr_stats.items import NyrrStatsItem

metadata_re = re.compile(r"<b>(.+):.+</b>(.+)<br>")
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
        for i in self.linkextractor.extract_links(response):
            req.append(Request(i.url, callback = self.parseRaces))
        return req

    def parseRaces(self, response):
        req = FormRequest.from_response(response,
            formdata = {"items.display":"500"},
            callback=self.parseRace)
        return req
    
    def parseRace(self,response):
        hxs = HtmlXPathSelector(response);
        rn =  hxs.select('//title/text()').extract()
        metadata = hxs.select("//span[@class='text']").extract()[0]
        parsedMetadata =  metadata_re.findall(metadata)
        print metadata[0]

        for name, value in parsedMetadata:
            if name=='Distance':
                raceDistMiles = value.split(" ")[0]
            
            #if name=='Date/Time':
            #    dateTime = #DO STUFF

            #if name=='Weather':
                #DO STUFF

            #if name=='Location':
                






        #item = NyrrStatsItem(raceName = rn[0])
        #print item['raceName']
        #return [item]

