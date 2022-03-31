# # # # # # # # # # # # # #
# INFINITE SCROLL SCRAPER #
# # # # # # # # # # # # # #

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request
import csv

# initialize spider class
class AsianSpider(scrapy.Spider):

    name = 'asian_food_spider'
    start_urls = ['https://www.asianmarketineurope.com/']
    allowed_domains = ['asianmarketineurope.com']

    headers = {
        
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
    }

    custom_settings = {
        'DOWNLOAD_DELAY': 2
        }

    # init method to create the csv file
    def __init__(self):
        
        print('[+]Creating the csv file...[+]')
        
        with open('food_items.csv', 'w') as food_csv:
            food_csv.write('Name,Price,Fat,Carbohydrates,Protein,Salt,Allergens,Ingredients\n')
            
        print('[+]csv file successfully created![+]')
                
    # spider's entry point
    def start_requests(self):

        # how many pages you want to extract data from?
        for page in range(1, 4): # 3 pages
            next_page = f"{self.start_urls[0]}?page={str(page)}"
            yield Request(url=next_page, headers=self.headers, callback=self.parse)
            

    def parse(self, response):

        print('****Parsing!****')

        # list of link to extract data from
        cards = [
            link for link in response.xpath("//a[@class='_29CWl']/@href").getall()
        ]

        for card in cards:
            yield response.follow(
            url=card,
            headers=self.headers,
            callback=self.parse_details
            )
            
    def parse_details(self, response):

        try:    
            features = {

                'Name': response.xpath("//h1[@class='_2qrJF']//text()").get(),
                'Price': response.xpath("//span[@data-hook='formatted-primary-price']//text()").get(),
                'Fat': response.xpath("//div[@class='WncCi']/p[3]//text()").get()[-5:],
                'Carbohydrates': response.xpath("//div[@class='WncCi']/p[4]//text()").get()[-5:],
                'Protein': response.xpath("//div[@class='WncCi']/p[5]//text()").get()[-5:],
                'Salt': response.xpath("//div[@class='WncCi']/p[6]//text()").get()[-5:],
                'Allergenes': response.xpath("//div[@class='rah-static rah-static--height-zero']//text()").get(),
                'Ingredients': response.xpath("//pre[@class='_28cEs']/p[4]//text()").get(),

                }
            
             # write features to our csv file 
            with open('food_items.csv', 'a') as food_csv:
                csv_writer = csv.DictWriter(food_csv, fieldnames=features.keys())
                csv_writer.writerow(features)
            
        except TypeError:
            print("A feature might be missing!")
            
            
# main driver
if __name__ == '__main__':

    process = CrawlerProcess()
    process.crawl(AsianSpider)
    process.start()

