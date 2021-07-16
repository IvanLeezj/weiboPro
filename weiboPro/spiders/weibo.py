from scrapy import Request, Spider
import json

from weiboPro.items import *


class WeiboSpider(Spider):
    name = 'weibo'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['http://www.xxx.com/']

    user_url = 'https://weibo.com/ajax/profile/info?uid={uid}'                            # 用户详情

    weibo_url = 'https://weibo.com/ajax/statuses/mymblog?uid={uid}&page={page}&feature=0'   # 微博列表

    follow_url = 'https://weibo.com/ajax/friendships/friends?page={page}&uid={uid}'        # 关注列表

    start_users = ['1227368500']

    def start_requests(self):
        for uid in self.start_users:
            yield Request(self.user_url.format(uid=uid), callback=self.parse_user)


    def parse_user(self, response):
        result = json.loads(response.text)
        user_info = result.get('data').get('user')
        field_map = {
            'description': 'description',
            'id': 'id',
            'followers_count': 'followers_count',
            'friends_count': 'friends_count',
            'location': 'location',
            'screen_name': 'screen_name',
            'verified_reason': 'verified_reason'
        }
        if user_info:
            item = UserItem()
            for key, value in field_map.items():
                item[key] = user_info.get(value)
            yield item

            uid = user_info.get('id')
            yield Request(self.follow_url.format(page=1, uid=uid), callback=self.parse_follows,
                          meta={'page': 1, 'uid': uid})

            yield Request(self.weibo_url.format(uid=uid, page=1), callback=self.parse_weibos,
                          meta={'page': 1, 'uid': uid})

    def parse_follows(self, response):
        result = json.loads(response.text)
        follow_info = result.get('users')                   # 获得一个列表
        dic = {}

        if result.get('next_cursor') != 0:
            for user_dict in follow_info:
                dic[user_dict.get('idstr')] = user_dict.get('name')
                if user_dict.get('idstr'):
                    uid = user_dict.get('idstr')
                    yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

            uid = response.meta.get('uid')
            item = UserRelationItem()
            item['id'] = uid
            item['follows'] = list(dic)
            yield item

            page = response.meta.get('page') + 1
            yield Request(self.follow_url.format(uid=uid, page=page), callback=self.parse_follows, meta={'page':page, 'uid':uid})

    def parse_weibos(self, response):
        result = json.loads(response.text)
        weibo_info = result.get('data').get('list')         # 获得一个列表
        field_map = {
            'id':'id',
            'attitudes_count': 'attitudes_count',
            'comments_count': 'comments_count',
            'create_at': 'create_at',
            'reposts_count': 'reposts_count',
            'text_raw': 'text_raw'
        }
        if result.get('data').get('bottom_tips_visible') == False:
            for weibo in weibo_info:
                item = WeiboItem()
                # item['id'] = response.meta.get('uid')
                for key, value in field_map.items():
                    item[key] = weibo.get(value)
                yield item
            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1
            yield Request(self.weibo_url.format(uid=uid, page=page), callback=self.parse_weibos,
                          meta={'uid': uid, 'page': page})
        else:
            print('-------------------此人微博已全部爬取------------------------')



