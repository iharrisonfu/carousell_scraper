import scrapy
import re
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse

from carousell_scraper.items import UserInfo, ItemInfo, ReviewDetail, UserFollower, UserFollowing

'''
from urllib.parse import urlencode

API_KEY = ''
def get_proxy_url(url):
    payload = {'api_key' : API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url
'''

class CarousellSpiderSpider(scrapy.Spider):
    name = "carousell_spider"
    allowed_domains = ["www.carousell.com.hk"]
    start_urls = ["https://www.carousell.com.hk/categories/computers-tech-461/desktops-5308"]
    
    def __init__(self):
        self.service = Service(executable_path="C:/Users/Harrison/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service)
        #self.driver = webdriver.Chrome() # Use ChromeDriverManager to install the latest chromedriver (https://pypi.org/project/webdriver-manager/
    
    '''
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
    '''
    
    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(1)  # Wait for page to load
        
        # click 'show more results' button to show more news
        page = 0
        page_limit = 2
        timeout = 2
        
        while page < page_limit:
            try:
                show_more_button = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[2]/div/section[3]/div[1]/div/button'))
                )
                self.driver.execute_script("arguments[0].click();", show_more_button)
                time.sleep(1)
                page += 1
            except:
                break
            
        # Create a Scrapy HtmlResponse from the Selenium WebDriver's page source
        body = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')
        #self.driver.quit()

        # locate listing card block
        user_item_block = response.css('div[data-testid^="listing-card"]')
        print(len(user_item_block))
        for uib in user_item_block:
            userUrl = 'https://www.carousell.com.hk/u/' + uib.css('a')[0].attrib['href'].split('/')[-2]
            userReviewsUrl = userUrl + '/reviews/'
            userFollowersUrl = userUrl + '/followers/'
            userfollowingUrl = userUrl + '/following/'
            
            itemUrl = uib.css('a')[1].attrib['href']
            
            yield response.follow(userUrl, callback=self.parse_user_page)
            yield response.follow(userReviewsUrl, callback=self.parse_userReview_page)
            yield response.follow(userFollowersUrl, callback=self.parse_userFollower_page)
            yield response.follow(userfollowingUrl, callback=self.parse_userFollowing_page)

    def parse_user_page(self, response):
        self.driver.get(response.url)
        time.sleep(2)

        # click 'show more results' button to show more news
        page = 0
        page_limit = 2
        timeout = 2
        
        while page < page_limit:
            try:
                show_more_button = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[1]/div[1]/div[3]/div[2]/div/div/div/button'))
                )
                self.driver.execute_script("arguments[0].click();", show_more_button)
                time.sleep(1)
                page += 1
            except:
                break
        
        # Create a Scrapy HtmlResponse from the Selenium WebDriver's page source
        body = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')
        
        # store user info
        # user info block
        user_info = response.xpath('//*[@id="main"]/div[1]/div[1]/div[3]/div[1]')
        for ui in user_info:
            # user name
            user_name = ui.xpath('.//h2/text()').getall()
            
            if "@" not in user_name:
                user_name = user_name[0]
                user_info_part1 = ui.xpath('.//p[1]/text()').getall()
                user_info_part2 = ui.xpath('.//p[2]/text()').getall()
                
                user_id = user_info_part1[1]
                user_rating = user_info_part1[2]
            
                if user_rating != 'No ratings yet':
                    user_rating_num = user_info_part2[0]
                    user_location = user_info_part2[1]
                else:
                    user_rating_num = 0
                    user_location = user_info_part2[0]
                
                user_joined_date = user_info_part2[-1]
                
                user_label = user_info_part1[4]
                
                if user_info_part1[-1] != 'Advertisement':
                    user_description = user_info_part1[-3]
                else:
                    user_description = None
            else:
                user_name = user_name[1]
                user_id = user_name
                
                user_info_part1 = ui.xpath('.//p[1]/text()').getall()
                user_info_part2 = ui.xpath('.//p[2]/text()').getall()
                
                user_rating = user_info_part1[0]
                
                if user_rating != 'No ratings yet':
                    user_rating_num = user_info_part2[0]
                else:
                    user_rating_num = 0
                user_location = user_info_part1[1]
                user_joined_date = user_info_part1[3]
            
                user_label = user_info_part1[5]
                
                if user_info_part1[-1] != 'Advertisement':
                    user_description = user_info_part1[-3]
                else:
                    user_description = None
                    
            userInfo = UserInfo()
            
            userInfo['user_id'] = user_id
            userInfo['user_name'] = user_name
            userInfo['user_rating'] = user_rating
            userInfo['user_rating_num'] = user_rating_num
            userInfo['user_location'] = user_location
            userInfo['user_joined_date'] = user_joined_date
            userInfo['user_label'] = user_label
            userInfo['user_description'] = user_description
            
            yield userInfo
            
        listing_cards = response.css('div[data-testid^="listing-card"]')

        for lcard in listing_cards:
            # locate item url
            item_url = lcard.css('a')[0].attrib['href']
            
            # locate item title
            item_title = lcard.xpath('/div[1]/a/p[1]/text()').get()
            
            yield response.follow(item_url, callback=self.parse_item_page)
    
    def parse_item_page(self, response):
        self.driver.get(response.url)
        time.sleep(2)
        
        # Create a Scrapy HtmlResponse from the Selenium WebDriver's page source
        body = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')
        
        # item title
        title = response.css('h1[data-testid="new-listing-details-page-desktop-text-title"] ::text').get()
        # seller
        seller = response.css('div[data-testid="new-listing-details-page-desktop-div-seller-contact-header"]')
        # category
        category_list = response.css('li[property="itemListElement"]')
        category = []
        for i in range(len(category_list)):
            category.append(category_list[i].css('a p ::text').get())
        # price
        price = response.css('div[id="FieldSetField-Container-field_price"] h2 ::text').get()
        # overview
        overview = response.css('div[id="FieldSetField-Container-field_sticky_info"]')
        # condition
        condition = response.css('div[id="FieldSetField-Container-field_condition_with_action"] span ::text').get() + ' # ' + response.css('div[id="FieldSetField-Container-field_condition_description"] span ::text').get()
        # description
        description = response.css('div[id="FieldSetField-Container-field_description_info"] p ::text').getall() + response.css('div[id="FieldSetField-Container-field_description"] p ::text').getall()
        # meet up
        meet_up = response.css('div[id="FieldSetField-Container-field_meetups_viewer"] p ::text').get()
        # pics
        pics_list = response.css('img[src^="https://media.karousell.com/media/photos/products"]')
        pics = []
        for i in range(len(pics_list)):
            pics.append(pics_list[i].attrib['src'])
            
        itemInfo = ItemInfo()
        
        itemInfo['item_title'] = title
        itemInfo['item_url'] = response.url
        itemInfo['seller_id'] = seller.css('a').attrib['href']
        itemInfo['item_category'] = category
        itemInfo['item_price'] = price
        itemInfo['item_overview'] = overview.css('span ::text').getall()
        itemInfo['item_condition'] = condition
        itemInfo['item_description'] = description
        itemInfo['meet_up'] = meet_up
        itemInfo['item_pics'] = pics

        yield itemInfo
        
    def parse_userReview_page(self, response):
        self.driver.get(response.url)
        time.sleep(2)
        
        # click the 'load more' button to load the whole review page
        page = 0
        page_limit = 5
        timeout = 1
        
        while page < page_limit:
            try:
                show_more_button = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[1]/div[1]/div[3]/div[2]/div/button'))
                )
                self.driver.execute_script("arguments[0].click();", show_more_button)
                time.sleep(1)
                page += 1
            except:
                break
            
        # Create a Scrapy HtmlResponse from the Selenium WebDriver's page source
        body = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')
        review_cards = response.css('li')
        
        for rcard in review_cards: 
            # locate reviewer id
            reviewer_id = rcard.css('a[data-testid="reviewr-name"]')[0].attrib['href']
            
            # locate reviwer is seller or buyer
            review_from = rcard.xpath('.//a[@data-testid="reviewr-name"]/following-sibling::span[1]/text()').get()

            # locate review date
            review_date = rcard.xpath('.//a[@data-testid="reviewr-name"]/following-sibling::span[2]/text()').get()
            
            # locate review label
            try:
                review_labels = rcard.css('img[src^="https://media.karousell.com/media/review_compliments"]')
                
                review_label = []
                for rlabel in review_labels:
                    review_label.append(rlabel.attrib['alt'])
                    
                review_label = ', '.join(review_label)
            except:
                review_labels = None
                
            # locate review rating
            review_rating = rcard.css('div[data-testid="star-rating"]')[0].attrib['aria-label']
            
            # locate review content
            review_content = rcard.css('p[data-testid="feedback-review"] ::text').get()
            
            # locate review item
            review_item = rcard.xpath('.//div/div/div/div[2]/div/div/div/div/p[1]/text()').get()
            
            reviewDetail = ReviewDetail()
            
            reviewDetail['reviewee_id'] = response.url.split('/')[-3]
            reviewDetail['reviewer_id'] = reviewer_id
            reviewDetail['review_from'] = review_from
            reviewDetail['review_date'] = review_date
            reviewDetail['review_label'] = review_label
            reviewDetail['review_rating'] = review_rating
            reviewDetail['review_content'] = review_content
            reviewDetail['review_item'] = review_item
            
            yield reviewDetail
            
    def parse_userFollower_page(self, response):
        self.driver.get(response.url)
        time.sleep(2)
        
        # click the 'load more' button to load the whole review page
        page = 0
        page_limit = 5
        timeout = 1
        
        while page < page_limit:
            try:
                show_more_button = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[1]/div[1]/div[3]/div[2]/div/div[3]/button'))
                )
                self.driver.execute_script("arguments[0].click();", show_more_button)
                time.sleep(1)
                page += 1
            except:
                break
            
        # Create a Scrapy HtmlResponse from the Selenium WebDriver's page source
        body = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')
        follower_cards = response.css('a[href^="/u/"]')
        
        for fc in follower_cards:
            userFollower = UserFollower()
            userFollower['user_id'] = response.url.split('/')[-3]
            userFollower['follower_id'] = fc.attrib['href']
            
            yield userFollower
        
    def parse_userFollowing_page(self, response):
        self.driver.get(response.url)
        time.sleep(2)
        
        # click the 'load more' button to load the whole review page
        page = 0
        page_limit = 5
        timeout = 1
        
        while page < page_limit:
            try:
                show_more_button = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[1]/div[1]/div[3]/div[2]/div/div[3]/button'))
                )
                self.driver.execute_script("arguments[0].click();", show_more_button)
                time.sleep(1)
                page += 1
            except:
                break
            
        # Create a Scrapy HtmlResponse from the Selenium WebDriver's page source
        body = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')
        follower_cards = response.css('a[href^="/u/"]')
        
        for fc in follower_cards:
            userFollowing = UserFollowing()
            userFollowing['user_id'] = response.url.split('/')[-3]
            userFollowing['following_id'] = fc.attrib['href']
            
            yield userFollowing
    


            
        
