from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class NYRRSpider(BaseSpider):
    linkextractor = SgmlLinkExtractor("result\.id=")
    name = "nyrr"
    allowed_domains = ["web2.nyrrc.org"]
    start_urls = [
        "http://web2.nyrrc.org/cgi-bin/start.cgi/aes-programs/results/resultsarchive.htm",
    ]
    
    def parse(self, response):
        req = []
        for i in range(2007,2012):
            req.append(FormRequest.from_response(response,
                formdata = {"NYRRYEAR":str(i)}), 
                callback=self.parse2)

    def parse2(self, response): 
        print self.linkextractor.extract_links(response)
        
