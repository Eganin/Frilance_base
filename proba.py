import requests
import bs4
from config import dict_ru_en
import csv
import os


class Telemetr_parser(object):
    def __init__(self, category: str, base_url: str):
        self.base_url = base_url
        self.params = {}
        self.session = requests.Session()
        self.headers = {
            'accept': '*/*',
            'user-agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.138 Chrome/81.0.4044.138 Safari/537.36'
        }
        self.category = category
        self.fieldnamed = ['title', 'brand_name', 'price']

    def get_url(self):
        r = self.session.get(url=self.base_url, params=self.params)

        return r

    def get_pagination(self, text):
        soup = bs4.BeautifulSoup(text.content, 'lxml')
        pagination = soup.select('li.nums')

        return int(pagination[-1].text.strip())

    def parametring(self, number: int):
        self.params['page'] = number

    def main_parser(self, web_page):
        soup = bs4.BeautifulSoup(web_page.content, 'lxml')
        data_all = []
        main_tovar = soup.select('div.catalog-item')
        for i in main_tovar:
            try:
                title = i.select_one('div.title').text
                print(title)

            except:
                title = ''

            try:
                brand = i.select_one('div.brand').text
                print(brand)

            except:
                brand = ''

            try:
                price = i.select_one('div.price.span')
                print(price)

            except Exception as e:
                print(e)
                price = '45'

            data = {
                'title': title,
                'brand_name': brand,
                'price': price
            }
            data_all.append(data)

        return data_all

    def csv_writer(self, data):
        try:
            with open('text.csv', 'a') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnamed)
                writer.writeheader()
                for data in data:
                    writer.writerow(data)

        except:
            with open('text.csv', 'w+') as file:
                pass

            with open('text.csv', 'a') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnamed)
                writer.writeheader()
                for data in data:
                    writer.writerow(data)

    def csv_clear(self):
        if os.path.exists('text.csv'):
            os.remove('text.csv')


def parser_category(category):
    result = ''
    for i in category:
        result += dict_ru_en[i]

    return str(result)


def main():
    category = str(input('Введите название нужной категории' + '\n ')).lower()
    base_url = 'https://www.autorus.ru/catalog/' + parser_category(category)
    print(base_url)
    clf = Telemetr_parser(category, base_url)
    content = clf.get_url()
    number = clf.get_pagination(content)
    clf.csv_clear()
    for i in range(1, number + 1):
        print(i)
        clf.parametring(i)
        web_page = clf.get_url()
        result = clf.main_parser(web_page)
        clf.csv_writer(result)


if __name__ == '__main__':
    main()
