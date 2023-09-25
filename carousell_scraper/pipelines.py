# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
#from scrapy.conf import settings
import json
from carousell_scraper.items import UserInfo, ItemInfo, ReviewDetail, UserFollower, UserFollowing

class CarousellScraperPipeline:
    def process_item(self, item, spider):
        # connect to mysql 
        conn = pymysql.connect(host="localhost",user="root",passwd='******',db="dd",use_unicode=True, charset="utf8")
        cur = conn.cursor()             
        print("mysql connected successfully!")
        
        # mysql storage logic
        '''########################################################
                        store user info into userInfo table             
            ########################################################'''
        if isinstance(item, UserInfo):
            try:
                # 8 fields
                user_id = item["user_id"]
                user_name = item["user_name"]
                user_rating = item["user_rating"]
                user_rating_num = item["user_rating_num"]
                user_location = item["user_location"]
                user_joined_date = item["user_joined_date"]
                user_label= item["user_label"]
                user_description = item["user_description"]

                sql = "INSERT INTO userInfo(user_id, user_name, user_rating, user_rating_num, user_location, user_joined_date, user_label, user_description) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % \
                                        (user_id, user_name, user_rating, user_rating_num, user_location, user_joined_date, user_label, user_description)
                print(sql)
            except Exception as err:
                print(err,'ERORR1!')

            try:
                cur.execute(sql)         # 真正执行MySQL语句，即查询TABLE_PARAMS表的数据
                print("insert user info successfully!")  # 测试语句
            except Exception as err:
                print(err)
                conn.rollback() #事务回滚,为了保证数据的有效性将数据恢复到本次操作之前的状态.有时候会存在一个事务包含多个操作，而多个操作又都有顺序，顺序执行操作时，有一个执行失败，则之前操作成功的也会回滚，即未操作的状态
            else:
                conn.commit()   #当没有发生异常时，提交事务，避免出现一些不必要的错误
            
            '''########################################################
                        store item info into itemInfo table             
            ########################################################'''
        elif isinstance(item, ItemInfo):
            try:
                # 10 fields
                item_title = item["item_title"]
                item_url = item["item_url"]
                seller_id = item["seller_id"]
                item_category = item["item_category"]
                item_price = item["item_price"]
                item_overview = item["item_overview"]
                item_condition = item["item_condition"]
                item_description = item["item_description"]
                meet_up = item["meet_up"]
                item_pics = item["item_pics"]
                
                sql2 = "INSERT INTO itemInfo(item_title, item_url, seller_id, item_category, item_price, item_overview, item_condition, item_description, meet_up, item_pics) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                            (item_title, item_url, seller_id, item_category, item_price, item_overview, item_condition, item_description, meet_up, item_pics)
                print(sql2)
                
            except Exception as err:
                print(err,'ERORR2!')
                
            try:
                cur.execute(sql2)
                print("insert item info successfully!")
            except Exception as err:
                print(err)
                conn.rollback()
            else:
                conn.commit()
        
            '''########################################################
                        store review detail into reviewDetail table             
            ########################################################'''
        elif isinstance(item, ReviewDetail):
            try:
                # 8 fields
                reviewee_id = item["item_title"]
                reviewer_id = item["item_title"]
                review_from = item["item_title"]
                review_date = item["item_title"]
                review_label = item["item_title"]
                review_rating = item["item_title"]
                review_content = item["item_title"]
                review_item = item["item_title"]
                
                sql3 = "INSERT INTO reviewDetail(reviewee_id, reviewer_id, review_from, review_date, review_label, review_rating, review_content, review_item) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                            (reviewee_id, reviewer_id, review_from, review_date, review_label, review_rating, review_content, review_item)
                print(sql3)
                
            except Exception as err:
                print(err,'ERORR2!')
                
            try:
                cur.execute(sql3)
                print("insert review detail successfully!")
            except Exception as err:
                print(err)
                conn.rollback()
            else:
                conn.commit()
                
            '''########################################################
                        store review detail into reviewDetail table             
            ########################################################'''
        elif isinstance(item, UserFollower):
            try:
                # 2 fields
                user_id = item["user_id"]
                follower_id = item["follower_id"]
                
                sql4 = "INSERT INTO userFollower(user_id, follower_id) VALUES ('%s', '%s')" % \
                                            (user_id, follower_id)
                print(sql4)
                
            except Exception as err:
                print(err,'ERORR4!')
                
            try:
                cur.execute(sql4)
                print("insert user follower successfully!")
            except Exception as err:
                print(err)
                conn.rollback()
            else:
                conn.commit()
                
            '''########################################################
                        store review detail into reviewDetail table             
            ########################################################'''
        elif isinstance(item, UserFollowing):
            try:
                # 2 fields
                user_id = item["user_id"]
                following_id = item["following_id"]
                
                sql5 = "INSERT INTO userFollowing(user_id, following_id) VALUES ('%s', '%s')" % \
                                            (user_id, following_id)
                print(sql5)
                
            except Exception as err:
                print(err,'ERORR5!')
                
            try:
                cur.execute(sql5)
                print("insert user following successfully!")
            except Exception as err:
                print(err)
                conn.rollback()
            else:
                conn.commit()

        conn.close()



        return item