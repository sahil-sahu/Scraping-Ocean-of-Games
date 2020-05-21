import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from scrapy.crawler import CrawlerProcess
dict = {
	# 'BOT_NAME' : 'hyper_scraping',
	# 'SPIDER_MODULES' : ['hyper_scraping.spiders'],
	# 'NEWSPIDER_MODULE' : 'hyper_scraping.spiders',
	'ROBOTSTXT_OBEY' : False,
	'DOWNLOADER_MIDDLEWARES' : {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,},

	}
class Game(scrapy.Spider):
	name = 'play'
	start_urls = ['http://oceanofgames.com/'
				 ]
	x=''
	naam = []	
	def parse(self,response):
		x = 'Call of Duty'
		# x = input('Please Input Song Name ::::::::::::::  ')
		return FormRequest.from_response(response,formdata={'s':x},callback=self.temp)
	def temp(self,response):
		n = 1
		k='Start'
		links = []
		while k!='stop':
			b_tag = response.xpath('/html/body/div[1]/div/div[2]/div/div/div/div/div[1]/div/div[3]/div['+str(n)+']/div/h2/a/text()').extract_first()
			a_tag = response.xpath('/html/body/div[1]/div/div[2]/div/div/div/div/div[1]/div/div[3]/div['+str(n)+']/div/h2/a/@href').extract_first()
			if a_tag == [] or a_tag==None :
				k='stop'
			else:
				links.append(a_tag)
				getattr(Game,'naam').append(b_tag)
				yield {'a_tag':a_tag,'b_tag':b_tag}
				n+=1	
		# x=int(input('Select Song Or the Movie Num('+str(n)+') == '))
		x=1
		# Game.x=x-1
		# yield {'x':getattr(Mrjatt,'x'),'naam':getattr(Mrjatt,'naam'),'type':getattr(Mrjatt,'link_type'),}
		yield response.follow(links[1],callback=self.temper)
	def temper(self,response):
		imgs = response.xpath('//*[(@id = "primary-content")]//*[contains(concat( " ", @class, " " ), concat( " ", "author-admin", " " ))]').extract()
		download_link = response.xpath('//*[(@id = "primary-content")]//form/@action').extract()				
		download_data = response.xpath('//*[(@id = "primary-content")]//form/input/@value').extract()				
		yield {'images':download_data,'download':download_link}
		yield FormRequest.from_response(response,formdata={'filename': download_data[0],'filesize':download_data[1],'id': download_data[2]},callback=self.endgame)

		# yield response.follow('https://www.pdfdrive.com'+download_link,callback=self.endgame)	
	def endgame(self,response):
		open_in_browser(response)
				
process = CrawlerProcess(settings=dict)	
process.crawl(Game)
process.start()