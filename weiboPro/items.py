# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class UserItem(scrapy.Item):
    collection = 'users'
    description = scrapy.Field()
    id = scrapy.Field()
    followers_count = scrapy.Field()
    friends_count = scrapy.Field()
    location = scrapy.Field()
    screen_name = scrapy.Field()
    verified_reason = scrapy.Field()


class UserRelationItem(scrapy.Item):
    collection = 'users'
    id = scrapy.Field()
    follows = scrapy.Field()


class WeiboItem(scrapy.Item):
    collection = 'weibo'
    id = scrapy.Field()
    attitudes_count = scrapy.Field()
    comments_count = scrapy.Field()
    create_at = scrapy.Field()
    reposts_count = scrapy.Field()
    text_raw = scrapy.Field()
