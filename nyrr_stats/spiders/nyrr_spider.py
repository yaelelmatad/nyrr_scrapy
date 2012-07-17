from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

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
        racename =  hxs.select('//title/text()').extract()
        metadata = hxs.select("//span[@class='text']").extract()[0].split('<br>')
        print metadata
        #raceinfo = hxs.select('//
