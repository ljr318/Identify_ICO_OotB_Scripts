import requests
from bs4 import BeautifulSoup
import json
import time


class IcoHtmlSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        }
        self.retry_count = 0

    # 1. Send Request
    def get_response(self, url):
        while True:
            if self.retry_count < 2:
                try:
                    res = requests.get(url, headers=self.headers)
                    soup = BeautifulSoup(res.text, 'lxml')
                    self.retry_count = 0
                    return soup.prettify()
                except Exception as e:
                    print(e)
                    print("\n Now retry to connect to " + url + "\n")
                    time.sleep(5)
                    self.retry_count += 1
                    continue
            else:
                print("Request to " + url + " failed\n")
                self.retry_count = 0
                return "error"

    # 2. Save Data
    @staticmethod
    def save_data(html_metadata, name):
        with open("ICO_Sanitized_Htmls//" + name + '.html', 'w', encoding='utf-8') as f:
            f.write(html_metadata)

    # 3. Launch
    def run(self):
        with open('ICO_Sanitized_Urls.json', 'r') as f:
            items = json.load(f)
        for item in items:
            # 1. Concatenate URL
            url = item['ICO URL']
            name = item['ICO name']
            # 2. Send request
            print("Start get html metadata on:" + url + "\n")
            data = self.get_response(url)
            if data == "error":
                continue
            # 3. Save data
            self.save_data(data, name)


IcoHtmlSpider().run()
