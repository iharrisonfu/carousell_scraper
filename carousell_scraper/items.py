# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
    
class UserInfo(scrapy.Item):
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_rating = scrapy.Field()
    user_rating_num = scrapy.Field()
    user_location = scrapy.Field()
    user_joined_date = scrapy.Field()
    user_label= scrapy.Field()
    user_description = scrapy.Field()
    
class ItemInfo(scrapy.Item):
    item_title = scrapy.Field()
    item_url = scrapy.Field()
    seller_id = scrapy.Field()
    item_category = scrapy.Field()
    item_price = scrapy.Field()
    item_overview = scrapy.Field()
    item_condition = scrapy.Field()
    item_description = scrapy.Field()
    meet_up = scrapy.Field()
    item_pics = scrapy.Field()
    
class ReviewDetail(scrapy.Item):
    reviewee_id = scrapy.Field()
    reviewer_id = scrapy.Field()
    review_from = scrapy.Field()
    review_date = scrapy.Field()
    review_label = scrapy.Field()
    review_rating = scrapy.Field()
    review_content = scrapy.Field()
    review_item = scrapy.Field()
    
class UserFollower(scrapy.Item):
    user_id = scrapy.Field()
    follower_id = scrapy.Field()
    
class UserFollowing(scrapy.Item):
    user_id = scrapy.Field()
    following_id = scrapy.Field()