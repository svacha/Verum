
import re
import scrapy

class MemberBioSpider(scrapy.Spider):
    """A Spider that crawls the member bios"""
    name = 'member_bio'
    allowed_domains = ['ncleg.net']
    
    
    def __init__(self):
        self.BASE_URL = 'http://www.ncleg.net'
        self.URL_PATTERN = r'/gascripts/members/viewMember.pl\?sChamber=(House|Senate)&nUserID=\d+'
        self.start_urls = ['http://www.ncleg.net/gascripts/members/memberList.pl?sChamber=House', 'http://www.ncleg.net/gascripts/members/memberList.pl?sChamber=Senate']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.get_member_pages)
            
    def get_member_pages(self, response):
        hrefs = response.css('a::attr(href)').extract()
        member_links = [href for href in hrefs if re.match(self.URL_PATTERN, href)]
        for member_link in member_links:
            full_url = self.BASE_URL + member_link
            yield scrapy.Request(url=full_url, callback=self.parse_bio)
         
    def parse_bio(self, response):
        member_dict = {}
        member_dict['title'] = response.css('#titleMemberBio::text').extract_first()
        return member_dict 
