import requests
from bs4 import BeautifulSoup
from lxml import etree
import json
import time


class IcoUrlSpider(object):
    def __init__(self):
        self.base_url = 'http://icobench.com/icos?page='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        }
        self.result_list = []
        self.retry_count = 0

    # 1. Send Request
    def get_response(self, url):
        while True:
            if self.retry_count < 5:
                try:
                    res = requests.get(url, headers=self.headers)
                    soup = BeautifulSoup(res.content.decode(), 'lxml')
                    self.retry_count = 0
                    return soup.prettify()
                except requests.exceptions.RequestException as e:
                    print(e)
                    print("\n Now retry to connect to " + url + "\n")
                    time.sleep(5)
                    self.retry_count += 1
                    continue
            else:
                print("Request to " + url + " failed\n")
                self.retry_count = 0
                return "error"

    def get_ico_url(self, url):
        try:
            data = self.get_response("http://icobench.com" + url)
            if data == "error":
                return
            x_data = etree.HTML(data)
            result_url = x_data.xpath('//a[@class="button_big"]/@href')
            result_name = x_data.xpath('//*[@id="profile_header"]/div//h1[@class = "notranslate"]/text()')
            print("Got URL: " + result_url[0])
            item = {
                "ICO name" : result_name[0],
                "ICO URL" : result_url[0]
            }
            self.result_list.append(item)
        except Exception as e:
            print(e)

    @staticmethod
    # 2. Parse Data
    def get_links(data):
        try:
            x_data = etree.HTML(data)
            result = x_data.xpath('//a[@class="name notranslate"]/@href')
            print(result)
            return result
        except Exception as e:
            print(e)

    # 3. Save Data
    def save_data(self):
        data_str = json.dumps(self.result_list)
        with open('ICO_Website_Urls.json', 'w', encoding='utf-8') as f:
            f.write(data_str)

    # 4. Launch
    def run(self):
        page = 477
        for i in range(1, page):
            # 1. Concatenate URL
            url = self.base_url + str(i)
            # 2. Send request
            data = self.get_response(url)
            if data == "error":
                continue
            # 3. Get links
            print("Start get links on page:" + str(i) + "\n")
            links = self.get_links(data)
            for link in links:
                self.get_ico_url(link)

        # 4. Save data
        self.save_data()


IcoUrlSpider().run()
