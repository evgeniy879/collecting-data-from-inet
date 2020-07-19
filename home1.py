import json
import requests


class Catalog:
    count = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
    }
    params = {'records_per_page': 50}

    replace = (',', '-', '/', '\\', '*', '"', '\n')

    def __init__(self, url):
        self.__url = url


    def categories(self, param=0):
        categories = []
        url_categories = 'https://5ka.ru/api/v2/categories/'
        data = requests.get(url_categories, headers=self.headers, params=self.params).json()
        for i in data:
            if param == 1:
                categories.append(i['parent_group_code'])
            else:
                categories.append(i['parent_group_name'])
        return categories


    def parse(self):
        cat = self.categories(1)
        for i in cat:
            params = {'records_per_page': 20, 'categories': i}
            url = 'https://5ka.ru/api/v2/special_offers/'
            items = []
            while url:
                response = requests.get(url, headers=self.headers, params=params)
                data = response.json()
                url = data['next']
                params = {}
                items.extend(data['results'])
            else:
                name = self.categories(0)[self.count]
                for j in self.replace:
                    name = name.replace(j, '')
                with open(f'{name}.json', 'w', encoding='UTF-8') as file:
                    json.dump(items, file, ensure_ascii=False)
                    self.count += 1



if __name__ == '__main__':
    catalog = Catalog('https://5ka.ru/api/v2')
    catalog.parse()
    print(1)