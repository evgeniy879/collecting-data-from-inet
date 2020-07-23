from bs4 import BeautifulSoup as bs
import requests
import json
import os

class GbBlogParse:
    domain = 'https://geekbrains.ru'
    url = 'https://geekbrains.ru/posts'
    catalog = []

    # сборка солянки
    def get_page_soup(self, url):
        response = requests.get(url)
        soup = bs(response.text, 'lxml')
        return soup

    # получение ссылочной массы на статьи в формате domain + пост
    def get_posts_urls(self, soup):
        posts_wrap = soup.find('div', attrs={'class': 'post-items-wrapper'})
        a_list = [f'{self.domain}{a.get("href")}' for a in
              posts_wrap.find_all('a', attrs={'class': 'post-item__title'})]
        return a_list

    # это пагинация, выдает по одной странице, начиная с 2.
    def pagination(self, soup):
        link = soup .find('ul', attrs={'class': 'gb__pagination'}).find_all('li', attrs={'class': 'page'})[-1] \
            .find('a', attrs={'rel': 'next'})
        return f'{self.domain}{link["href"]}' if link else None


    def save_to_file(self):
        name = 'data'
        file_path = os.path.join(os.getcwd(), f'{name}.json')
        with open(file_path, 'w', encoding='UTF-8') as file:
            json.dump(self.catalog, file, ensure_ascii=False)


    # это парсер + сборщик требуемых данных.
    def run(self):
        url_ = self.url
        while url_:
            soup_ = self.get_page_soup(url_)
            links_post = self.get_posts_urls(soup_)
            for posts in links_post:
                soup_data = self.get_page_soup(posts)
                title = soup_data.find('h1').string
                name = soup_data.find('div', attrs={'class': 'col-md-5 col-sm-12 col-lg-8 col-xs-12 padder-v'}) \
                .find('a').find('div', attrs={'class': 'text-lg text-dark'}).string
                link = soup_data.find('div', attrs={'class': 'col-md-5 col-sm-12 col-lg-8 col-xs-12 padder-v'}) \
                .find('a')['href']
                profile = f'{self.domain}{link}'
                info = {'title_post': title, 'author_name': name, 'author_url': profile, 'url_post': posts}
                self.catalog.append(info)
            url_ = self.pagination(soup_)
            print(url_)
        else:
            self.save_to_file()


if __name__ == '__main__':
    test = GbBlogParse()
    test.run()
    print(1)
