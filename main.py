import requests
import bs4
import os
import csv
import json


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
        self.fieldnamed = ['href', 'image', 'title', 'location', 'price', 'phone_number', 'owners_name', 'description',
                           'area', 'pool', 'type', 'parking', 'condition', 'furnishing', 'postal_code',
                           'air_conditioning', 'no_of_bedrooms', 'no_of_bathrooms']
        self.soup = bs4.BeautifulSoup(self.get_url().content, 'lxml')

    def get_url(self, item_url=None):
        if item_url:
            r = self.session.get(url=item_url)

        else:
            r = self.session.get(url=self.base_url, params=self.params)

        return r

    def get_pagination(self):
        pagination = self.soup.select('a.page-number.js-page-filter')

        return int(pagination[-1].text.strip())

    def parametring(self, number: int):
        self.params['page'] = number

    def main_parser(self, web_page) -> list:
        soup = bs4.BeautifulSoup(web_page.content, 'lxml')
        data_all = []
        tables = soup.select('a.mask')
        for i in tables:
            data_all.append('https://www.bazaraki.com' + str(i['href']))

        return data_all

    def csv_clear(self):
        if os.path.exists('text.csv'):
            os.remove('text.csv')

    def parsing_pagination(self, url_page: list) -> list:
        for i in url_page:
            data_home = []
            images_new = []
            r_web_page = self.get_url(i)
            soup_home = bs4.BeautifulSoup(r_web_page.content, 'lxml')
            images = soup_home.select('img', attrs={'itemprop': "image"})
            for j in images:
                if str(j)[12:24] == 'similar__img':
                    pass

                if str(j['src'][8:24]) == 'cdn.bazaraki.com' and len(str(j)) > 110:
                    images_new.append(j['src'])

            try:
                title = soup_home.select_one('h1#ad-title.title-announcement').text.strip()

            except:
                title = ' '

            try:
                location = soup_home.select_one(
                    'a.announcement__location.js-open-announcement-location').span.text.strip()

            except:
                location = ''

            try:
                price = soup_home.select_one('div.announcement-price__cost').text.strip()

            except:
                price = ''

            try:
                phone_number = soup_home.select_one('span.phone-author-subtext__main').text.strip()

            except:
                phone_number = ''

            try:
                owners_name = soup_home.select_one('p.author-name.js-online-user').text.strip()

            except:
                owners_name = ''

            try:
                description = soup_home.select_one('div.announcement-description').text.strip()

            except:
                description = ''

            for table in soup_home.select('div.announcement-characteristics.clearfix'):
                t = table.find_all('a')
                try:
                    area = t[0].text

                except:
                    area = ''

                try:
                    pool = t[1].text

                except:
                    pool = ''

                try:
                    type = t[2].text

                except:
                    type = ''

                try:
                    parking = t[3].text

                except:
                    parking = ''

                try:
                    condition = t[4].text

                except:
                    condition = ''

                try:
                    furnishing = t[5].text

                except:
                    furnishing = ''

                try:
                    postal_code = t[6].text

                except:
                    postal_code = ''

                try:
                    air_conditioning = t[7].text

                except:
                    air_conditioning = ''

                try:
                    no_of_bedrooms = t[8].text

                except:
                    no_of_bedrooms = ''

                try:
                    no_of_bathrooms = t[9].text

                except:
                    no_of_bathrooms = ''

            data_h = {'href': i,
                      'image': images_new,
                      'title': title,
                      'location': location,
                      'price': price,
                      'phone_number': phone_number,
                      'owners_name': owners_name,
                      'description': description,
                      'area': area,
                      'pool': pool,
                      'type': type,
                      'parking': parking,
                      'condition': condition,
                      'furnishing': furnishing,
                      'postal_code': postal_code,
                      'air_conditioning': air_conditioning,
                      'no_of_bedrooms': no_of_bedrooms,
                      'no_of_bathrooms': no_of_bathrooms}
            print(data_h)
            data_home.append(data_h)

            return data_home

    def clear_file(self):
        if os.path.exists('text.csv'):
            os.remove('text.csv')

        if os.path.exists('text.xlsx'):
            os.remove('text.xlsx')

        with open('text.csv', 'w+') as file:
            pass

        with open('text.xlsx', 'w+') as file:
            pass

    def writer(self, data_all: list, output: str):
        if output == 'csv' or output == 'xlsx':
            try:
                with open('text.' + str(output), 'a') as file:
                    writer = csv.DictWriter(file, fieldnames=self.fieldnamed)
                    writer.writeheader()
                    for data in data_all:
                        writer.writerow(data)

            except:
                pass

        elif output == 'json':
            result_data = []
            for data in data_all:
                json_dict = json.dumps(data)
                result_data.append(json_dict)

            return result_data


def main():
    output = str(input('В каком формате вам вывести резульат csv или xlsx  или json '))
    category = str(
        input('Введите название города , введите пробел если все города учитывая регистр сайта ' + '\n ')).lower()
    if category:
        base_url = 'https://www.bazaraki.com/real-estate/' + str(category) + '/'

    else:
        base_url = 'https://www.bazaraki.com/real-estate/'
    clf = Telemetr_parser(category, base_url)
    number = clf.get_pagination()
    clf.csv_clear()
    clf.clear_file()
    for i in range(1, number + 1):
        clf.parametring(i)
        web_page = clf.get_url()
        result = clf.main_parser(web_page)
        parsing = clf.parsing_pagination(result)
        clf.writer(parsing, output)


if __name__ == '__main__':
    main()
