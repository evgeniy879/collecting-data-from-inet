import scrapy
import re
import json
from copy import deepcopy
from scrapy.loader import ItemLoader
from avito_parse.items import PaginationUserInstagram


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    graphql_ = 'https://www.instagram.com/graphql/query/?'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    api_query = {'posts_feed': 'bfa387b2992c3a52dcbe447467b4b771'}
    variabals = {"id": None, "first": 12}


    def __init__(self, login: str, passwd: str, parse_users: list, *args, **kwargs):
        self.parse_users = parse_users
        self.login = login
        self.passwd = passwd
        super().__init__(*args, **kwargs)

    def parse(self, response):
        token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.login_url,
                                 method='POST',
                                 callback=self.im_login,
                                 formdata={'username': self.login,
                                           'enc_password': self.passwd},
                                 headers={'X-CSRFToken': token})

    def im_login(self, response):
        data = response.json()
        if data['authenticated']:
            for user_name in self.parse_users:
                yield response.follow(f'/{user_name}',
                                      callback=self.user_parse,
                                      cb_kwargs={'user_name': user_name})

    def user_parse(self, response, user_name):
        user_id = self.fetch_user_id(response.text, user_name)
        variables = deepcopy(self.variabals)
        variables['id'] = f"{user_id}"
        url = f"{self.graphql_}query_hash={self.api_query['posts_feed']}&variables={json.dumps(variables)}"
        yield response.follow(url,
                              callback=self.user_feed_parse,
                              cb_kwargs={'user_name': user_name, 'variables': variables})

    def user_feed_parse(self, response, user_name, variables):
        data = response.json()
        for i in data['data']['user']['edge_owner_to_timeline_media']['edges']:
            item = ItemLoader(PaginationUserInstagram())
            item.add_value('user_name', user_name)
            item.add_value('user_id', variables['id'])
            item.add_value('post_pub_date', i['node']['taken_at_timestamp'])
            item.add_value('like_count', i['node']['edge_media_preview_like']['count'])
            item.add_value('post_photos', i['node']['display_url'])
            yield item.load_item()

        if data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']:
            variables['after'] = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            url = f"{self.graphql_}query_hash={self.api_query['posts_feed']}&variables={json.dumps(variables)}"
            yield response.follow(url,
                                  callback=self.user_feed_parse,
                                  cb_kwargs={'user_name': user_name, 'variables': variables})


    def fetch_user_id(self, text, username):
        matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' %username, text).group()
        return json.loads(matched).get('id')

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')
